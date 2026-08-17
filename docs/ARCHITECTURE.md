# Architecture overview

## Request flow (stock page)

```mermaid
sequenceDiagram
    participant Browser
    participant Django
    participant Summary as stock_summary
    participant Redis
    participant Yahoo

    Browser->>Django: GET /stock/AAPL/summary/
    Django->>Summary: build_stock_summary(AAPL)
    par Parallel fetches
        Summary->>Redis: bio, news, fundamentals
        Summary->>Yahoo: cache miss → fetch
    end
    Summary->>Summary: TA metrics + patterns
    Summary->>Summary: build_decision_verdict()
    Summary->>Summary: build_trade_plan()
    Summary-->>Django: JSON
    Django-->>Browser: verdict + trade_plan + data
```

## Services layer

| Service | Responsibility |
|---------|----------------|
| `stock_data.py` | Yahoo fetches: bio, news, fundamentals, holders, earnings, charts |
| `technical_metrics.py` | TA: crossover, ADX, Bollinger, RSI, candle/harmonic patterns |
| `screener_cache.py` | Cache Yahoo screeners; Celery refresh |
| `stock_summary.py` | Orchestrate parallel fetches + verdict + trade plan |
| `decision_verdict.py` | Buy / Hold / Sell verdict |
| `trade_plan.py` | Entry, stop, targets, position hint |

Views in `frontend_app/views.py` are thin HTTP wrappers: validate symbol, call service, return `JsonResponse`. Shared helpers live in `symbols.py`, `http_responses.py`, and `view_helpers.py`.

## Docker services

| Service | Role |
|---------|------|
| `web` | Django (dev: runserver, prod: Gunicorn) |
| `nginx` | Production reverse proxy + static files |
| `worker` | Celery tasks |
| `beat` | Scheduled screener refresh |
| `db` | PostgreSQL |
| `redis` | Cache, sessions, Celery broker |

## Key endpoints

See [README](../README.md#main-api-endpoints).

## Related docs

- [DECISION_VERDICT.md](DECISION_VERDICT.md)
- [TRADE_PLAN.md](TRADE_PLAN.md)
