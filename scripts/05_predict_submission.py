#!/usr/bin/env python3
"""Predict the official test metadata using a trusted, local baseline artifact.

IMPORTANT: joblib is pickle-based. Only load artifacts you created and trust.
"""
import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from k12mlops.features import ALLOWED, metadata_text


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    p.add_argument("--model", type=Path, default=Path("models/baseline.joblib"))
    p.add_argument("--out", type=Path, default=Path("reports/baseline_submission.csv"))
    args = p.parse_args()
    # Only trust local model files; DO NOT load arbitrary serialized joblib from strangers.
    artifact = joblib.load(args.model)
    if tuple(artifact["allowed_features"]) != tuple(ALLOWED):
        raise SystemExit("Serving feature contract mismatches trained model")
    test = pd.read_csv(args.data_dir / "test.csv", dtype={"trace_id": str})
    sample = pd.read_csv(args.data_dir / "sample_submission.csv", dtype=str)
    if not set(ALLOWED).issubset(test.columns) or "trace_id" not in test:
        raise SystemExit("Test file doesn't satisfy inference feature contract")
    if test.trace_id.duplicated().any():
        raise SystemExit("Duplicate test trace_id")
    if sample.shape[1] != 2:
        raise SystemExit("Expected sample submission with ID + one prediction column; review Kaggle docs")
    id_column, label_column = sample.columns
    if id_column != "trace_id":
        raise SystemExit(f"Unexpected submission key {id_column!r}; inspect official sample before adapting")
    if set(sample[id_column]) != set(test.trace_id):
        raise SystemExit("Sample and test ID sets differ")
    model = artifact["pipeline"]
    probs = model.predict_proba([metadata_text(r) for r in test.to_dict("records")])
    classes = np.asarray(model.named_steps["classifier"].classes_)
    order = np.argsort(-probs, axis=1, kind="stable")[:, :min(3, len(classes))]
    ranks = [" ".join(str(classes[j]) for j in row) for row in order]
    mapping = dict(zip(test.trace_id.astype(str), ranks))
    sample[label_column] = sample[id_column].astype(str).map(mapping)
    if sample[label_column].isna().any():
        raise SystemExit("Missing prediction for some rows")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise SystemExit(f"Refusing to overwrite {args.out}")
    sample.to_csv(args.out, index=False)
    print(f"Created {len(sample)}-row submission: {args.out}; format copied from official sample")
    print("This is a metadata-only system smoke test; it is NOT competitive.")


if __name__ == "__main__":
    main()
