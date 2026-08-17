# Sector & peer comparison

Compare a stock against Yahoo Finance recommended peers on valuation and quality metrics.

## Stock page

On `/stock/<symbol>/`, open **Fundamental Analysis → Peer comparison**. The table shows:

- The subject symbol (highlighted)
- Up to 5 peer symbols from Yahoo `recommendedSymbols`
- Metrics: P/E, Forward P/E, ROE, ROA, operating margin, current ratio, revenue growth YoY, dividend yield

Sector and industry come from the subject bio. **Sector P/E** is shown in the section header when available.

Peer data is also included in `GET /stock/<symbol>/summary/` under `peers`.

## Financial health chart

The financial health chart loads peer rows (net debt/EBITDA, interest coverage, current ratio, quick ratio) via `GET /stock/<symbol>/finacial_health_chart/`.

## API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/stock/<symbol>/peers/` | No | Peer comparison JSON |
| `GET` | `/stock/<symbol>/summary/` | No | Includes `peers` in bundle |

### Query params

- `limit` — number of peers (1–10, default 5)

### Example response shape

```json
{
  "symbol": "AAPL",
  "sector": "Technology",
  "subject": { "symbol": "AAPL", "is_subject": true, "metrics": { ... } },
  "peers": [ { "symbol": "MSFT", "metrics": { ... } } ],
  "metrics": [ { "key": "trailingPE", "label": "P/E (TTM)" } ],
  "averages": { "trailingPE": 28.5 }
}
```

Peers depend on Yahoo data; some symbols may return an empty peer list.
