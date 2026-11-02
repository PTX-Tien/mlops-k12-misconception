#!/usr/bin/env python3
"""Freeze a reproducible validation split; GROUP by question_id (not official split)."""
import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    p.add_argument("--out", type=Path, default=Path("data/processed/split.csv"))
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--test-size", type=float, default=0.2)
    args = p.parse_args()
    df = pd.read_csv(args.data_dir / "train.csv", dtype={"trace_id": str, "question_id": str})
    needed = {"trace_id", "question_id", "root_code"}
    if not needed.issubset(df.columns):
        raise SystemExit(f"train.csv must have {sorted(needed)}")
    if df[list(needed)].isna().any().any() or df.trace_id.duplicated().any():
        raise SystemExit("Missing/duplicate key columns: fix data contract first")
    if not 0 < args.test_size < 1:
        raise SystemExit("--test-size must be between 0 and 1")
    splitter = GroupShuffleSplit(n_splits=1, test_size=args.test_size, random_state=args.seed)
    tr, va = next(splitter.split(df, df.root_code, groups=df.question_id))
    split = df[["trace_id", "question_id", "root_code"]].copy()
    split["split"] = "train"
    split.iloc[va, split.columns.get_loc("split")] = "val"
    if set(split.iloc[tr].question_id) & set(split.iloc[va].question_id):
        raise AssertionError("Question group leakage!")
    if set(split.iloc[tr].trace_id) & set(split.iloc[va].trace_id):
        raise AssertionError("Trace ID leakage!")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise SystemExit(f"Split already frozen at {args.out}; do not silently overwrite it")
    split[["trace_id", "split"]].to_csv(args.out, index=False)
    stats = {"seed": args.seed, "strategy": "group_question", "train_rows": len(tr),
             "validation_rows": len(va), "train_questions": int(df.iloc[tr].question_id.nunique()),
             "validation_questions": int(df.iloc[va].question_id.nunique()),
             "train_labels": int(df.iloc[tr].root_code.nunique()),
             "validation_labels": int(df.iloc[va].root_code.nunique()),
             "validation_labels_not_in_train": sorted(set(df.iloc[va].root_code) - set(df.iloc[tr].root_code))}
    args.out.with_suffix(".manifest.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))
    print(f"Frozen: {args.out}")


if __name__ == "__main__":
    main()
