"""Builds preprocessing, base models and the stacking ensemble from configs/run.toml.

Paper settings come from Table 3 (UNSW-NB15 column); everything else is a
logged choice in docs/DEVIATIONS.md (D3-D5, D9, D10, D12).
"""
from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (FunctionTransformer, MinMaxScaler, OneHotEncoder,
                                   PowerTransformer, StandardScaler)
from sklearn.svm import SVC
import numpy as np


def preprocessor(cfg: dict) -> ColumnTransformer:
    p = cfg["preprocess"]
    cat = cfg["features"]["categorical"]
    num = [f for f in cfg["features"]["names"] if f not in cat]

    steps = []
    if p["numeric_transform"] == "yeo-johnson":
        steps.append(("power", PowerTransformer(method="yeo-johnson", standardize=False)))
    elif p["numeric_transform"] == "log1p":
        steps.append(("log1p", FunctionTransformer(np.log1p, feature_names_out="one-to-one")))
    elif p["numeric_transform"] != "none":
        raise ValueError(f"unknown numeric_transform {p['numeric_transform']}")
    steps.append(("scale", StandardScaler() if p["scaler"] == "standard" else MinMaxScaler()))
    num_pipe = Pipeline(steps)

    if p["categorical_encoding"] == "onehot":
        cat_pipe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    elif p["categorical_encoding"] == "hashing":
        cat_pipe = Pipeline([
            ("to_dict", FunctionTransformer(lambda X: [{str(v): 1} for v in np.asarray(X).ravel()])),
            ("hash", FeatureHasher(n_features=p["hashing_n_features"], input_type="dict")),
            ("dense", FunctionTransformer(lambda X: X.toarray())),
        ])
    else:
        raise ValueError(f"unknown categorical_encoding {p['categorical_encoding']}")

    return ColumnTransformer([("num", num_pipe, num), ("cat", cat_pipe, cat)], remainder="drop")


def base_models(cfg: dict, seed: int) -> list[tuple[str, object]]:
    m = cfg["models"]
    return [
        ("rf", RandomForestClassifier(n_estimators=m["rf_n_estimators"], criterion=m["rf_criterion"],
                                      random_state=seed, n_jobs=-1)),
        ("knn", KNeighborsClassifier(n_neighbors=m["knn_n_neighbors"], metric=m["knn_metric"], n_jobs=-1)),
        ("lr", LogisticRegression(penalty=m["lr_penalty"], max_iter=m["lr_max_iter"], random_state=seed)),
    ]


def meta_model(cfg: dict) -> SVC:
    m = cfg["models"]
    return SVC(C=m["svm_C"], kernel=m["svm_kernel"], gamma=m["svm_gamma"])


def stacking_pipeline(cfg: dict, seed: int) -> Pipeline:
    s = cfg["stacking"]
    stack = StackingClassifier(
        estimators=base_models(cfg, seed),
        final_estimator=meta_model(cfg),
        cv=StratifiedKFold(n_splits=s["cv_folds"], shuffle=True, random_state=seed),
        stack_method=s["stack_method"],
        passthrough=s["passthrough"],
    )
    return Pipeline([("prep", preprocessor(cfg)), ("stack", stack)])


def single_pipeline(cfg: dict, model) -> Pipeline:
    return Pipeline([("prep", preprocessor(cfg)), ("model", model)])
