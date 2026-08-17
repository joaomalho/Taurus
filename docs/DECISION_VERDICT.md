# Decision verdict (Phase 1)

The investment verdict appears at the top of each stock page (`/stock/<symbol>/`).

## Output

| Field | Description |
|-------|-------------|
| `verdict` | `Buy`, `Hold`, or `Sell` |
| `confidence` | 35–95% based on signal strength |
| `score` | Combined bias from -1 (bearish) to +1 (bullish) |
| `reasons` | Up to 6 bullet points explaining the verdict |
| `components` | Breakdown of fundamental, technical, and analyst inputs |

## Formula

```
combined = 0.45 × fundamental_bias + 0.55 × technical_bias + analyst_modifier
```

### Fundamental bias

- Derived from pillar score (0–10) via `backend/risk_manager/scoring.py`
- `(score - 5) / 5`, clamped to [-1, 1]

### Technical bias

- Average of directional signals:
  - EMA crossover → Buy / Sell / Flat
  - Bollinger Bands → Buy / Sell / Flat
  - RSI → Buy / Sell / Flat
- ADX modifier:
  - `< 20` → TA weight halved (weak trend)
  - `≥ 25` → noted as trend support

### Analyst modifier

- Yahoo `recommendationMean` (1 = Strong Buy … 5 = Strong Sell)
- Small adjustment (±0.25 max)

### Thresholds

| Combined score | Verdict |
|----------------|---------|
| ≥ 0.30 | Buy |
| ≤ -0.30 | Sell |
| otherwise | Hold |

## Implementation

- Service: `market-analyzer/frontend_app/services/decision_verdict.py`
- Included in: `GET /stock/<symbol>/summary/` → field `verdict`
- UI: `displayDecisionVerdict()` in `static/js/display.js`

## Disclaimer

Advisory only — not financial advice. The verdict synthesizes automated signals; always validate before trading.
