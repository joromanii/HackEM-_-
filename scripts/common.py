"""Shared helpers: config, data loading, run folders and run records.

Every script that produces results writes a new run folder (refusing to
overwrite) with run_meta.json: config, versions, input checksums, git state
and runtime.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
import time
import tomllib
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "configs" / "run.toml"


def load_config(path: Path = DEFAULT_CONFIG) -> dict:
    with Path(path).open("rb") as f:
        return tomllib.load(f)


def resolve(value: str) -> Path:
    p = Path(value).expanduser()
    return p if p.is_absolute() else REPO_ROOT / p


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def data_paths(cfg: dict) -> tuple[Path, Path]:
    d = resolve(cfg["paths"]["data_dir"])
    return d / cfg["paths"]["train_file"], d / cfg["paths"]["test_file"]


def load_split(path: Path) -> pd.DataFrame:
    # utf-8-sig: the official files start with a byte-order mark
    df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    return df


def load_train_test(cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    tr, te = data_paths(cfg)
    return load_split(tr), load_split(te)


def check_features(df: pd.DataFrame, names: list[str]) -> None:
    missing = [n for n in names if n not in df.columns]
    if missing:
        raise SystemExit(f"STOP: feature columns missing from data: {missing}")


def new_run_dir(cfg: dict, kind: str, name: str, out_dir: Path | None = None) -> Path:
    out = out_dir or resolve(cfg["paths"]["results_dir"]) / kind / f"{dt.date.today().isoformat()}_{name}"
    if out.exists():
        raise SystemExit(f"Refusing to overwrite existing run folder: {out}")
    out.mkdir(parents=True)
    return out


def git_info() -> dict:
    def run(*args: str) -> str:
        try:
            return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True,
                                  text=True, check=True).stdout.strip()
        except Exception as exc:
            return f"unavailable ({exc.__class__.__name__})"
    return {"commit": run("rev-parse", "HEAD"), "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty_files": run("status", "--porcelain")}


def package_versions() -> dict:
    from importlib.metadata import version
    out = {}
    for pkg in ["numpy", "pandas", "scikit-learn", "scipy"]:
        try:
            out[pkg] = version(pkg)
        except Exception:
            out[pkg] = "not installed"
    return out


class RunRecord:
    """Collects run metadata; call .save() at the end."""

    def __init__(self, script: str, cfg: dict, config_path: Path, out_dir: Path, inputs: list[Path]):
        self.t0 = time.time()
        self.out_dir = out_dir
        self.meta = {
            "script": script,
            "script_sha256": sha256_file(REPO_ROOT / script),
            "code_sha256": {p.name: sha256_file(p) for p in sorted((REPO_ROOT / "scripts").glob("*.py"))},
            "started": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "config_file": str(Path(config_path).resolve().relative_to(REPO_ROOT))
            if Path(config_path).resolve().is_relative_to(REPO_ROOT) else str(config_path),
            "config_sha256": sha256_file(config_path),
            "config": cfg,
            "inputs": {p.name: {"sha256": sha256_file(p), "bytes": p.stat().st_size} for p in inputs},
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "cpu_count": __import__("os").cpu_count(),
            "packages": package_versions(),
            "git": git_info(),
        }

    def save(self, **extra) -> None:
        self.meta["runtime_seconds"] = round(time.time() - self.t0, 1)
        self.meta.update(extra)
        (self.out_dir / "run_meta.json").write_text(json.dumps(self.meta, indent=2, default=str))


def binary_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray | None = None) -> dict:
    """Binary metrics with attack (1) as the positive class (proposed D14).

    FAR = FP / (FP + TN): normal records wrongly flagged as attack.
    """
    from sklearn.metrics import confusion_matrix, roc_auc_score
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    acc = (tp + tn) / (tp + tn + fp + fn)
    prec = tp / (tp + fp) if (tp + fp) else float("nan")
    rec = tp / (tp + fn) if (tp + fn) else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else float("nan")
    far = fp / (fp + tn) if (fp + tn) else float("nan")
    out = {"TP": int(tp), "TN": int(tn), "FN": int(fn), "FP": int(fp),
           "accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "far": far}
    out["auc"] = float(roc_auc_score(y_true, y_score)) if y_score is not None else float("nan")
    return out
