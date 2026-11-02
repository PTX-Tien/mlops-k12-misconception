#!/usr/bin/env python3
"""Data ingestion/contract audit — CPU only, does not change raw data."""
import argparse
import datetime as dt
import hashlib
import json
from collections import Counter
from pathlib import Path

import pandas as pd
from PIL import Image, UnidentifiedImageError

REQUIRED_INPUT = ["trace_id", "question_id", "grade", "topic_name", "question_text", "correct_answer", "image_file"]
REQUIRED_TRAIN = REQUIRED_INPUT + ["root_code", "transcription_steps"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for piece in iter(lambda: f.read(4 * 1024 * 1024), b""):
            digest.update(piece)
    return digest.hexdigest()


def check_image(dir_path: Path, relative_name: str) -> tuple[bool, str]:
    if not relative_name or relative_name == "nan":
        return False, "missing_filename"
    base = dir_path.resolve()
    target = (dir_path / relative_name).resolve()
    if not target.is_relative_to(base):
        return False, "path_outside_image_directory"
    if not target.is_file():
        return False, "file_missing"
    try:
        with Image.open(target) as im:
            im.verify()
    except (OSError, UnidentifiedImageError, ValueError):
        return False, "invalid_image"
    return True, "ok"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    ap.add_argument("--image-sample", type=int, default=12)
    ap.add_argument("--report", type=Path, default=Path("reports/data_audit.json"))
    args = ap.parse_args()
    root = args.data_dir.resolve()
    if not (root / "train.csv").is_file():
        raise SystemExit(f"Missing {root / 'train.csv'}; check archive nesting or Kaggle access")
    report = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "root": str(root), "tables": {}, "errors": [], "warnings": []}
    tables = {}
    for name in ("train", "test", "unlabelled", "sample_submission", "taxonomy_v1"):
        path = root / (name + ".csv")
        if not path.exists():
            report["warnings"].append(f"not found: {path.name}")
            continue
        df = pd.read_csv(path, dtype={"trace_id": str, "question_id": str}, low_memory=False)
        tables[name] = df
        rec = {"rows": len(df), "columns": list(df.columns),
               "sha256": sha256(path),
               "missing_fraction": {c: round(float(df[c].isna().mean()), 5) for c in df.columns}}
        if "trace_id" in df:
            rec["unique_trace_ids"] = int(df["trace_id"].nunique())
            if df["trace_id"].duplicated().any():
                report["errors"].append(f"{name}: duplicate trace_id")
        if "root_code" in df:
            rec["root_code_counts"] = dict(Counter(df["root_code"].fillna("<missing>").astype(str)))
        missing = sorted(set(REQUIRED_TRAIN if name == "train" else REQUIRED_INPUT) - set(df.columns)) if name in ("train", "test", "unlabelled") else []
        if missing:
            report["errors"].append(f"{name}: missing expected columns {missing}")
        report["tables"][path.name] = rec

    if "train" in tables and "test" in tables:
        t, v = tables["train"], tables["test"]
        if "trace_id" in t and "trace_id" in v:
            overlap = set(t.trace_id.dropna()) & set(v.trace_id.dropna())
            report["train_test_trace_id_overlap"] = len(overlap)
            if overlap:
                report["errors"].append("train/test trace_id overlap")
        if "question_id" in t and "question_id" in v:
            report["train_test_question_id_overlap"] = len(set(t.question_id) & set(v.question_id))
        # columns that are privileged MUST NOT be available to serving code
        forbidden = ["root_code", "transcription_steps", "final_answer_correct", "clean", "misconceptions"]
        report["test_has_privileged_columns"] = sorted(set(forbidden) & set(v.columns))
        if report["test_has_privileged_columns"]:
            report["warnings"].append("Unexpected privileged columns in test metadata; do not use")

    for part in ("train", "test", "unlabelled"):
        if part not in tables:
            continue
        df = tables[part]
        if "image_file" not in df:
            continue
        # For large unlabelled pool, verify only first deterministic sample.
        names = df["image_file"].dropna().astype(str).head(max(args.image_sample, 0))
        attempts = [check_image(root / "images" / part, name) for name in names]
        report[f"{part}_image_samples"] = {"checked": len(attempts), "issues": [
            {"file": name, "reason": outcome[1]} for name, outcome in zip(names, attempts) if not outcome[0]
        ]}
        if report[f"{part}_image_samples"]["issues"]:
            report["errors"].append(f"{part}: sampled image errors")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Audit saved to {args.report}; errors={len(report['errors'])}, warnings={len(report['warnings'])}")
    if report["errors"]:
        for error in report["errors"]:
            print("ERROR:", error)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
