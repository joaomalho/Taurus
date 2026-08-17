# Pivot points

Support and resistance levels derived from the previous session's high, low, and close.

## Methods

| Method | Description |
|--------|-------------|
| `classic` | Standard floor pivots (PP, R1–R3, S1–S3) |
| `fibonacci` | PP with 38.2%, 61.8%, and 100% extensions |
| `camarilla` | Intraday levels anchored on previous close |

## Reference period

Levels use the **previous daily bar** OHLC. The current bar close drives the signal.

## Signal

| Condition | Signal |
|-----------|--------|
| Price ≥ R1 | Sell (at resistance) |
| Price ≤ S1 | Buy (at support) |
| Otherwise | Flat |

Implementation: `backend/tecnical_analysis/pivot_points.py`, `RiskManagerTechnical.signal_decision_pivot()`.

## API

```
GET /stock/<symbol>/pivot_points/?method=classic
```

Also included in `GET /stock/<symbol>/summary/` as `pivot_points` (classic by default).

## Response schema

```json
{
  "symbol": "AAPL",
  "method": "classic",
  "reference_date": "2026-08-15T00:00:00",
  "reference_ohlc": { "high": 110, "low": 90, "close": 100 },
  "current_price": 104,
  "levels": {
    "pp": 100, "r1": 110, "r2": 120, "r3": 130,
    "s1": 90, "s2": 80, "s3": 70
  },
  "signal": "Flat"
}
```

## UI

Stock page → **Technical Analysis → Trend → Pivot Points**. Method selector + level table; nearest level (within 0.5%) is highlighted.

## Chart overlay

Pivot levels appear as horizontal lines on the **Historic Price** candlestick chart:

- **PP** — solid yellow
- **R1–R3** — dashed red tones
- **S1–S3** — dashed green tones

Toggle visibility with the eye icon in the chart legend (left side, **PP** row). Lines update when you click **Calculate** or on initial page load from `/summary/`.
