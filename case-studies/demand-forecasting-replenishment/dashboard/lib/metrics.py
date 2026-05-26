"""Forecast metric helpers for Favorita demand planning proof slice."""

from __future__ import annotations

from typing import Iterable, Optional


def _pairs(actual: Iterable[float], forecast: Iterable[float]) -> list[tuple[float, float]]:
    actual_values = list(actual)
    forecast_values = list(forecast)
    if len(actual_values) != len(forecast_values):
        raise ValueError("actual and forecast must have equal length")
    pairs = [(float(a), float(f)) for a, f in zip(actual_values, forecast_values)]
    if not pairs:
        raise ValueError("actual and forecast must contain at least one value")
    return pairs


def wape(actual: Iterable[float], forecast: Iterable[float]) -> Optional[float]:
    """Return WAPE percentage; None when actual demand denominator is zero."""
    pairs = _pairs(actual, forecast)
    denom = sum(abs(a) for a, _ in pairs)
    if denom == 0:
        return None
    value = sum(abs(a - f) for a, f in pairs) / denom * 100
    return round(value, 2)


def mae(actual: Iterable[float], forecast: Iterable[float]) -> float:
    """Return mean absolute error in demand units."""
    pairs = _pairs(actual, forecast)
    return round(sum(abs(a - f) for a, f in pairs) / len(pairs), 2)


def bias_pct(actual: Iterable[float], forecast: Iterable[float]) -> Optional[float]:
    """Return forecast bias percentage; negative means under-forecast."""
    pairs = _pairs(actual, forecast)
    denom = sum(abs(a) for a, _ in pairs)
    if denom == 0:
        return None
    value = sum(f - a for a, f in pairs) / denom * 100
    return round(value, 2)


def forecast_score(wape_pct: Optional[float], bias_pct_value: Optional[float]) -> Optional[float]:
    """Return bounded planning score from 0-100 using error and bias penalty."""
    if wape_pct is None or bias_pct_value is None:
        return None
    score = 100 - float(wape_pct) - abs(float(bias_pct_value))
    return round(max(0.0, min(100.0, score)), 2)


def fva(naive_wape: Optional[float], candidate_wape: Optional[float]) -> Optional[float]:
    """Return Forecast Value Added percentage vs naïve baseline."""
    if naive_wape in (None, 0) or candidate_wape is None:
        return None
    value = (float(naive_wape) - float(candidate_wape)) / float(naive_wape) * 100
    return round(value, 2)
