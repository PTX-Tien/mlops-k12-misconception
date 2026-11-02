"""Official-style single-label MAP@K and diagnostic metrics.

For one relevant code per row, AP@K equals reciprocal rank when found in top K.
"""
from collections.abc import Sequence


def reciprocal_rank_at_k(target: str, ranked: Sequence[str], k: int = 3) -> float:
    if k < 1:
        raise ValueError("k must be positive")
    if not isinstance(target, str) or not target:
        raise ValueError("target must be a nonempty string")
    seen: set[str] = set()
    for position, predicted in enumerate(ranked[:k], start=1):
        if predicted in seen:  # repeated labels must not yield additional credit
            continue
        seen.add(predicted)
        if predicted == target:
            return 1.0 / position
    return 0.0


def map_at_k(y_true: Sequence[str], y_ranked: Sequence[Sequence[str]], k: int = 3) -> float:
    if len(y_true) != len(y_ranked):
        raise ValueError("different number of targets/prediction rows")
    if not y_true:
        raise ValueError("empty evaluation set")
    return sum(
        reciprocal_rank_at_k(str(target), predicted, k)
        for target, predicted in zip(y_true, y_ranked)
    ) / len(y_true)


def diagnostic_metrics(y_true: Sequence[str], y_ranked: Sequence[Sequence[str]]) -> dict[str, float]:
    if len(y_true) != len(y_ranked) or not y_true:
        raise ValueError("nonempty aligned inputs required")
    top1 = [row[0] if row else "" for row in y_ranked]
    total = len(y_true)
    none_total = sum(label == "NONE" for label in y_true)
    none_predicted = sum(label == "NONE" for label in top1)
    none_tp = sum(y == "NONE" and p == "NONE" for y, p in zip(y_true, top1))
    return {
        "map_at_3": map_at_k(y_true, y_ranked, 3),
        "accuracy_at_1": sum(y == p for y, p in zip(y_true, top1)) / total,
        "recall_at_3": sum(y in pred[:3] for y, pred in zip(y_true, y_ranked)) / total,
        "none_precision": none_tp / none_predicted if none_predicted else 0.0,
        "none_recall": none_tp / none_total if none_total else 0.0,
        "false_alarm_rate_on_none": (none_total - none_tp) / none_total if none_total else 0.0,
        "n_validation": float(total),
        "n_none": float(none_total),
    }
