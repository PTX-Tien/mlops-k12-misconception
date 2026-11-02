#!/usr/bin/env python3
"""CPU metadata-only model for MLOps wiring, NOT competitive visual diagnosis."""
import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from k12mlops.features import ALLOWED, FORBIDDEN, metadata_text
from k12mlops.metrics import diagnostic_metrics


def checksum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def git_sha():
    p = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    return p.stdout.strip() if p.returncode == 0 else "uncommitted"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    ap.add_argument("--split", type=Path, default=Path("data/processed/split.csv"))
    ap.add_argument("--model", type=Path, default=Path("models/baseline.joblib"))
    ap.add_argument("--report", type=Path, default=Path("reports/baseline_metrics.json"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df = pd.read_csv(args.data_dir / "train.csv", dtype={"trace_id": str, "question_id": str})
    assign = pd.read_csv(args.split, dtype={"trace_id": str})
    required = set(ALLOWED) | {"trace_id", "root_code"}
    if not required.issubset(df.columns) or not {"trace_id", "split"}.issubset(assign):
        raise SystemExit("Data contract failed: missing columns")
    if df.trace_id.duplicated().any() or assign.trace_id.duplicated().any():
        raise SystemExit("Duplicate trace_id")
    if set(assign.trace_id) != set(df.trace_id) or set(assign.split) != {"train", "val"}:
        raise SystemExit("Split must be complete and contain exactly train/val")
    if set(FORBIDDEN) & set(ALLOWED):
        raise AssertionError("Forbidden feature entered feature list")
    combined = df.merge(assign, on="trace_id", validate="one_to_one")
    tr = combined[combined.split == "train"]
    va = combined[combined.split == "val"]
    if tr.empty or va.empty:
        raise SystemExit("Empty train or validation partition")
    if "question_id" in combined and (set(tr.question_id) & set(va.question_id)):
        raise SystemExit("Question group overlap: expected group-question protocol")
    if tr.root_code.isna().any() or va.root_code.isna().any():
        raise SystemExit("Missing target labels")
    if tr.root_code.nunique() < 2:
        raise SystemExit("Baseline requires at least 2 classes")

    x_train = [metadata_text(row) for row in tr.to_dict("records")]
    x_val = [metadata_text(row) for row in va.to_dict("records")]
    model = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 4), min_df=1,
                                   max_features=30000, sublinear_tf=True)),
        ("classifier", LogisticRegression(C=0.5, max_iter=400, class_weight="balanced",
                                           random_state=args.seed)),
    ])
    model.fit(x_train, tr.root_code.astype(str).tolist())
    probs = model.predict_proba(x_val)
    classes = np.asarray(model.named_steps["classifier"].classes_)
    order = np.argsort(-probs, axis=1, kind="stable")[:, :min(3, len(classes))]
    predictions = [[str(classes[j]) for j in rank] for rank in order]
    truth = va.root_code.astype(str).tolist()
    metrics = diagnostic_metrics(truth, predictions)
    metrics["number_of_train_classes"] = int(len(classes))
    metrics["n_train"] = int(len(tr))
    metrics["validation_unseen_class_rows"] = int(sum(y not in classes for y in truth))

    args.model.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    if args.model.exists():
        raise SystemExit(f"Model already exists: {args.model} (use a new version/path)")
    joblib.dump({"pipeline": model, "allowed_features": ALLOWED, "feature_version": "metadata-v1"}, args.model)
    predictions_path = args.report.with_name("baseline_val_predictions.csv")
    if predictions_path.exists():
        raise SystemExit(f"Predictions already exist: {predictions_path}")
    pd.DataFrame({"trace_id": va.trace_id.astype(str), "truth": truth,
                  "top3": [" ".join(row) for row in predictions]}).to_csv(predictions_path, index=False)
    report = {"metrics": metrics, "lineage": {
        "git_sha": git_sha(),
        "raw_train_csv_sha256": checksum(args.data_dir / "train.csv"),
        "split_csv_sha256": checksum(args.split),
        "model_sha256": checksum(args.model),
        "python": platform.python_version(),
        "sklearn": sklearn.__version__, "seed": args.seed,
        "feature_version": "metadata-v1", "features": list(ALLOWED),
        "limitations": "No handwriting/image information: pipeline smoke baseline only",
    }}
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["metrics"], indent=2))
    print(f"Model: {args.model}; report: {args.report}")


if __name__ == "__main__":
    main()
