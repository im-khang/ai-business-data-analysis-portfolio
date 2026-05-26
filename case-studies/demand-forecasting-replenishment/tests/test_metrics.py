import math
import sys
from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_ROOT / "dashboard"))

from lib.metrics import bias_pct, forecast_score, fva, mae, wape


def test_wape_returns_percentage_error():
    assert wape([100, 50, 50], [90, 60, 40]) == 15.0


def test_wape_zero_demand_returns_none():
    assert wape([0, 0, 0], [1, 2, 3]) is None


def test_mae_returns_unit_error():
    assert mae([10, 20, 30], [8, 18, 36]) == 3.33


def test_bias_pct_negative_means_under_forecast():
    assert bias_pct([100, 100], [80, 90]) == -15.0


def test_bias_pct_positive_means_over_forecast():
    assert bias_pct([100, 100], [120, 110]) == 15.0


def test_forecast_score_penalizes_error_and_bias():
    assert forecast_score(wape_pct=20.0, bias_pct_value=-10.0) == 70.0


def test_forecast_score_floor_zero():
    assert forecast_score(wape_pct=90.0, bias_pct_value=30.0) == 0.0


def test_fva_positive_when_candidate_beats_naive():
    assert fva(naive_wape=40.0, candidate_wape=30.0) == 25.0


def test_fva_negative_when_candidate_worse_than_naive():
    assert fva(naive_wape=40.0, candidate_wape=50.0) == -25.0


def test_fva_none_when_naive_zero_or_missing():
    assert fva(naive_wape=0.0, candidate_wape=10.0) is None
    assert fva(naive_wape=None, candidate_wape=10.0) is None


def test_mismatched_lengths_raise_value_error():
    import pytest
    with pytest.raises(ValueError, match="equal length"):
        wape([1, 2, 3], [1])
