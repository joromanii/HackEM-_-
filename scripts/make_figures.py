"""Figures for the report and slides (Issue #9), built only from saved results.

Reads results files (never retrains) and writes PNGs plus, for each figure,
the exact numbers plotted as a CSV (the table view), and figures.md with alt
text. Colors: validated reference palette, light mode; "ours" is always blue,
"paper" is always orange.

Usage:
  .venv/bin/python scripts/make_figures.py [--comparison DIR] [--error DIR]
        [--sttl DIR] [--multiclass DIR] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_CONFIG, REPO_ROOT, git_info, load_config, new_run_dir, package_versions, sha256_file  # noqa: E402

R = REPO_ROOT / "results"
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
OURS, PAPER, TRAIN = "#2a78d6", "#eb6834", "#1baf7a"   # palette slots 1, 2, 3

# paper-reported (Table 4, Table 6 recall %)
PAPER_T4 = {"accuracy": 0.94, "precision": 0.96, "recall": 0.93, "f1": 0.95, "auc": 0.99, "far": 0.052}
PAPER_T4_COUNTS = {"TP": 42535, "TN": 35365, "FN": 2797, "FP": 1635}
PAPER_T6_RECALL = {"Analysis": 11, "Backdoor": 10.79, "DoS": 25, "Exploits": 85, "Fuzzers": 60.97,
                   "Generic": 98.32, "Normal": 91.82, "Reconnaissance": 74.8, "Shellcode": 58.22, "Worms": 37.5}

plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                     "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.edgecolor": GRID, "font.size": 11, "axes.titlesize": 13, "axes.titleweight": "bold"})


def style(ax, axis="x"):
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis=axis, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def grouped_barh(ax, labels, series, fmt):
    """series: list of (name, values, color). Paper above ours in each group."""
    n, h, gap = len(series), 0.36, 0.04
    for k, (name, vals, color) in enumerate(series):
        ys = [i + (k - (n - 1) / 2) * (h + gap) for i in range(len(labels))]
        bars = ax.barh(ys, vals, height=h, color=color, label=name, edgecolor=SURFACE, linewidth=2)
        for b, v in zip(bars, vals):
            ax.text(b.get_width(), b.get_y() + b.get_height() / 2, " " + fmt(v), va="center", fontsize=9, color=INK2)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()


def save(fig, out, name, data: pd.DataFrame, alt: str, notes: list):
    fig.tight_layout()
    fig.savefig(out / f"{name}.png", dpi=200)
    plt.close(fig)
    data.to_csv(out / f"{name}.csv", index=False)
    notes.append((name, alt))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--comparison", type=Path, default=R / "comparison" / "2026-11-15_table4")
    p.add_argument("--error", type=Path, default=R / "runs" / "2026-11-15_error_analysis_stacking_seed42")
    p.add_argument("--sttl", type=Path, default=R / "runs" / "2026-11-15_sttl_profile")
    p.add_argument("--multiclass", type=Path, default=R / "runs" / "2026-11-15_stacking_multiclass_seed42")
    p.add_argument("--out-dir", type=Path, default=None)
    a = p.parse_args()
    t0 = time.time()
    cfg = load_config(DEFAULT_CONFIG)
    out = new_run_dir(cfg, "figures", "figures", a.out_dir)
    notes: list = []

    # 1. Table 4 metrics
    comp = pd.read_csv(a.comparison / "comparison.csv")
    names = {"accuracy": "Accuracy", "precision": "Precision", "recall": "Recall", "f1": "F1",
             "auc": "AUC", "far": "False alarm rate"}
    comp["label"] = comp["metric"].map(names)
    fig, ax = plt.subplots(figsize=(8, 5))
    grouped_barh(ax, comp["label"].tolist(),
                 [("Paper (Table 4)", comp["paper_table4"].tolist(), PAPER), ("Ours", comp["ours"].tolist(), OURS)],
                 lambda v: f"{v:.4f}".rstrip("0").rstrip(".") if v in PAPER_T4.values() else f"{v:.4f}")
    ax.set_xlim(0, 1.12)
    ax.set_xlabel("Score (0–1; false alarm rate: lower is better)")
    ax.set_title("Binary result on the UNSW-NB15 test set: paper vs ours")
    style(ax)
    ax.legend(loc="lower right", frameon=False)
    save(fig, out, "fig1_table4_metrics", comp[["metric", "paper_table4", "ours", "difference"]],
         "Grouped bars of six metrics. Ours is lower than the paper on accuracy (0.8648 vs 0.94), precision, "
         "F1 and AUC, higher on recall (0.9821 vs 0.93), and the false alarm rate is 0.2790 vs 0.052.", notes)

    # 2. Confusion counts
    cnt = pd.read_csv(a.comparison / "counts.csv")
    lab = {"TP": "TP: attack caught", "TN": "TN: normal passed", "FN": "FN: attack missed", "FP": "FP: normal flagged"}
    fig, ax = plt.subplots(figsize=(8, 4.2))
    grouped_barh(ax, [lab[c] for c in cnt["count"]],
                 [("Paper (Table 4)", cnt["paper_table4"].tolist(), PAPER), ("Ours", cnt["ours"].tolist(), OURS)],
                 lambda v: f"{int(v):,}")
    ax.set_xlim(0, max(cnt[["paper_table4", "ours"]].max()) * 1.18)
    ax.set_xlabel("Test records (82,332 in total)")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_title("Confusion counts: more attacks caught,\nfar more normal traffic flagged")
    style(ax)
    ax.legend(loc="lower right", frameon=False)
    save(fig, out, "fig2_confusion_counts", cnt,
         "Grouped bars of TP, TN, FN, FP. Ours: FN 810 vs paper 2,797; FP 10,322 vs paper 1,635.", notes)

    # 3. Where the false alarms are (by sttl)
    fp = pd.read_csv(a.error / "fp_by_sttl.csv")
    top = fp[fp["false_positives"] > 0].copy()
    top["sttl"] = top["sttl"].astype(str)
    fig, ax = plt.subplots(figsize=(8, 3.2))
    bars = ax.barh(top["sttl"], top["false_positives"], height=0.5, color=OURS, edgecolor=SURFACE, linewidth=2)
    for b, n, s in zip(bars, top["false_positives"], top["share_of_all_fp"]):
        ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" {n:,} ({s:.1%})", va="center", fontsize=9, color=INK2)
    ax.invert_yaxis()
    ax.set_xlim(0, top["false_positives"].max() * 1.3)
    ax.set_ylabel("sttl value")
    ax.set_xlabel("False alarms (normal test records flagged as attack)")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_title("87.4% of our false alarms are normal records with sttl = 254")
    style(ax)
    save(fig, out, "fig3_false_alarms_by_sttl", fp,
         "Bars of false alarms by sttl value: 9,025 at sttl 254 (87.4%) and 1,297 at sttl 62 (12.6%); none elsewhere. "
         "This shows where false alarms concentrate; it is not a tested cause.", notes)

    # 4. sttl = 254: attack vs normal, train vs test
    st = pd.read_csv(a.sttl / "sttl_by_split_label.csv")
    s254 = st[st["sttl"] == 254].pivot_table(index="split", columns="label", values="rows").reindex(["train", "test"])
    normal_share = st[(st["label"] == "normal")].pivot_table(index="sttl", columns="split", values="share_of_label_in_split").fillna(0)
    rows = []
    for v in [31, 254, 62, 0]:
        if v in normal_share.index:
            rows.append({"sttl": str(v), "train": normal_share.loc[v, "train"], "test": normal_share.loc[v, "test"]})
    ns = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    grouped_barh(ax, ns["sttl"].tolist(),
                 [("Training file", ns["train"].tolist(), TRAIN), ("Testing file", ns["test"].tolist(), OURS)],
                 lambda v: f"{v:.1%}")
    ax.set_xlim(0, 0.85)
    ax.set_ylabel("sttl value")
    ax.set_xlabel("Share of normal records")
    ax.set_title("Normal traffic with sttl = 254: 20% of training,\n41% of testing")
    style(ax)
    ax.legend(loc="lower right", frameon=False)
    sub = (f"In training, sttl = 254 is {int(s254.loc['train','attack']):,} attack vs {int(s254.loc['train','normal']):,} normal "
           f"rows; in testing {int(s254.loc['test','attack']):,} vs {int(s254.loc['test','normal']):,}.")
    fig.text(0.01, 0.01, sub, fontsize=8.5, color=INK2)
    save(fig, out, "fig4_normal_sttl_shift", ns,
         "Grouped bars of the share of normal records at each sttl value, training vs testing. sttl 31: 70.5% vs 45.1%; "
         "sttl 254: 20.1% vs 40.7%. " + sub, notes)

    # 5. Seeds and variants vs the paper
    seeds = pd.read_csv(a.comparison / "seeds.csv")
    var = pd.read_csv(a.comparison / "variants.csv") if (a.comparison / "variants.csv").exists() else pd.DataFrame()
    seeds = pd.concat([seeds[seeds["seed"] == 42], seeds[seeds["seed"] != 42]])
    pts = [("seed " + str(s) + (" (headline)" if s == 42 else ""), acc) for s, acc in zip(seeds["seed"], seeds["accuracy"])]
    pts += [(v, acc) for v, acc in zip(var.get("variant", []), var.get("accuracy", []))]
    dfp = pd.DataFrame(pts, columns=["run", "accuracy"])
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.scatter(dfp["accuracy"], range(len(dfp)), s=60, color=OURS, edgecolor=SURFACE, linewidth=2, zorder=3, label="Ours")
    for i, (r, v) in enumerate(pts):
        ax.text(v, i, f"   {v:.4f}", va="center", fontsize=9, color=INK2)
    ax.axvline(PAPER_T4["accuracy"], color=PAPER, linewidth=2)
    ax.text(PAPER_T4["accuracy"], len(pts) - 1, "Paper 0.94  ", ha="right", va="center", fontsize=10, color=INK2)
    ax.set_yticks(range(len(dfp)))
    ax.set_yticklabels(dfp["run"])
    ax.invert_yaxis()
    ax.set_xlim(0.85, 0.95)
    ax.set_xlabel("Accuracy on the test set (axis starts at 0.85)")
    ax.set_title("Six seeds and three preprocessing choices\nall land near 0.865 (ours, blue)")
    style(ax)
    save(fig, out, "fig5_seeds_variants", dfp,
         "Dots for six seeds and three preprocessing variants, all between 0.8640 and 0.8662, far left of the paper's 0.94 line. "
         "The x-axis starts at 0.85.", notes)

    # 6. Per-class recall (multiclass)
    pc = pd.read_csv(a.multiclass / "per_class_stacking.csv", index_col=0)
    classes = [c for c in PAPER_T6_RECALL]
    mc = pd.DataFrame({"class": classes, "paper_recall_pct": [PAPER_T6_RECALL[c] for c in classes],
                       "ours_recall_pct": [pc.loc[c, "recall"] * 100 for c in classes]})
    mc = mc.sort_values("paper_recall_pct", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    grouped_barh(ax, mc["class"].tolist(),
                 [("Paper (Table 6, 51,535-row subset)", mc["paper_recall_pct"].tolist(), PAPER),
                  ("Ours (full test set)", mc["ours_recall_pct"].tolist(), OURS)],
                 lambda v: f"{v:.1f}%")
    ax.set_xlim(0, 118)
    ax.set_xlabel("Recall (%)")
    ax.set_title("10-class recall: mostly the same easy and hard classes\n(exceptions: Shellcode higher, Normal lower)")
    style(ax)
    ax.legend(loc="lower right", frameon=False)
    save(fig, out, "fig6_multiclass_recall", mc.round(4),
         "Grouped bars of per-class recall. Both high for Generic, Exploits, Reconnaissance; both low for DoS, Analysis, "
         "Backdoor. Normal: paper 91.8%, ours 74.2%.", notes)

    md = ["# Figures", "", "Built by `scripts/make_figures.py` from saved results only. Each PNG has a CSV with the exact numbers "
          "plotted (table view). Ours = blue, paper = orange. Paper values `paper-reported`; ours `measured` (sources below).", ""]
    for name, alt in notes:
        md += [f"## {name}", "", f"![{alt}]({name}.png)", "", f"Alt text: {alt}", "", f"Data: [`{name}.csv`]({name}.csv)", ""]
    md += ["Sources: " + ", ".join(f"`{d.relative_to(REPO_ROOT)}`" for d in [a.comparison, a.error, a.sttl, a.multiclass])]
    (out / "figures.md").write_text("\n".join(md) + "\n")
    meta = {"script": "scripts/make_figures.py", "script_sha256": sha256_file(Path(__file__)),
            "inputs": {str(f.relative_to(REPO_ROOT)): sha256_file(f) for d in [a.comparison, a.error, a.sttl, a.multiclass]
                       for f in sorted(d.glob("*.csv"))},
            "runtime_seconds": round(time.time() - t0, 1),
            "python": sys.version.split()[0], "packages": {**package_versions(),
                                                          "matplotlib": matplotlib.__version__},
            "git": git_info(), "paper_values": {"table4": PAPER_T4, "table6_recall_pct": PAPER_T6_RECALL}}
    (out / "run_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Wrote {len(notes)} figures to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
