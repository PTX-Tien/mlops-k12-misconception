import pytest

from k12mlops.metrics import diagnostic_metrics, map_at_k, reciprocal_rank_at_k


def test_reciprocal_ranks():
    assert reciprocal_rank_at_k("CAL-01", ["CAL-01", "NONE", "OTH-00"]) == 1
    assert reciprocal_rank_at_k("CAL-01", ["NONE", "CAL-01", "OTH-00"]) == 0.5
    assert reciprocal_rank_at_k("CAL-01", ["NONE", "OTH-00", "CAL-01"]) == pytest.approx(1 / 3)
    assert reciprocal_rank_at_k("CAL-01", ["NONE", "OTH-00", "ANS-01"]) == 0


def test_map():
    targets = ["NONE", "CAL-01", "ANS-01", "WOP-01"]
    guesses = [["NONE"], ["NONE", "CAL-01"], ["NONE", "CAL-01", "ANS-01"], ["NONE"]]
    assert map_at_k(targets, guesses) == pytest.approx((1 + 0.5 + 1 / 3 + 0) / 4)
    metrics = diagnostic_metrics(targets, guesses)
    assert metrics["n_validation"] == 4
    assert metrics["false_alarm_rate_on_none"] == 0


def test_bad_input():
    with pytest.raises(ValueError):
        map_at_k(["A"], [])
    with pytest.raises(ValueError):
        map_at_k([], [])
    with pytest.raises(ValueError):
        reciprocal_rank_at_k("A", ["A"], k=0)
