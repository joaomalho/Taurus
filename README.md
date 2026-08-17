# Taurus

![Logo](https://github.com/joaomalho/Taurus/blob/main/assets/taurus.png?raw=true)

**Empowering investors with real-time financial insights.**

Taurus is a financial market analysis web application for stocks and ETFs. It combines technical analysis (TA-Lib), fundamental scoring, pattern detection, and a unified **Buy / Hold / Sell** verdict to support investment decisions.

> **Disclaimer:** All analysis is advisory only and does not constitute financial advice. Data comes from public APIs (mainly Yahoo Finance) and may be delayed or incomplete.

---

## Key features

### Decision support

- **Investment verdict** — unified Buy / Hold / Sell on each stock page, with confidence score and reasons
- **Trade plan** — entry, stop-loss, TP1/TP2, R:R, and position hint (when verdict is Buy or Sell)
- **Fundamental pillar scoring** — Valuation, Financial Health, Profitability, Growth, Dividends, Capital Efficiency
- **Watchlist** — save up to 50 symbols per user (dashboard + add from stock page)

### Technical analysis

- EMA crossovers, ADX, Bollinger Bands, RSI
- 40+ candlestick patterns (TA-Lib) with stop-loss logic
- Harmonic pattern backtesting
- Custom charts (financial health, profitability, efficiency, earnings)

### Fundamental analysis

- KPIs, valuations, insider transactions, institutional holders
- Analyst recommendations
- Financial statement Excel downloads (annual + quarterly)
- News feed per symbol

### Platform

- **Aggregated stock API** — `/stock/<symbol>/summary/` (single request for page load)
- **Redis caching** — Yahoo data, sessions, screener cache
- **Rate limiting** — protects public APIs from abuse
- **Celery + Beat** — background refresh of stock screeners (gainers, trending, most active)
- **Auth** — signup, login, password reset, protected stock-by-top page
- **CI** — GitHub Actions (Docker + Django tests)
- **Production stack** — Gunicorn + Nginx (`docker-compose.prod.yml`)

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11, Django 4.x |
| Database | PostgreSQL 15 |
| Cache / queue | Redis 7, Celery |
| Analysis | pandas, numpy, TA-Lib, yfinance |
| Frontend | Django templates, ES modules, Chart.js, lightweight-charts, Grid.js |
| Infra | Docker Compose, Gunicorn, Nginx |

---

## Quick start (development)

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone and configure

```bash
git clone https://github.com/joaomalho/Taurus.git
cd Taurus
cp .env.example .env
```

Edit `.env` only if you need custom credentials. Defaults work for local development.

### 2. Start the stack

```bash
docker compose up --build -d
docker compose logs -f web
```

### 3. Run migrations

```bash
docker compose exec web python manage.py migrate
```

### 4. Open the app

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Home — search stocks |
| http://localhost:8000/stock/AAPL/ | Stock analysis page |
| http://localhost:8000/signup/ | Create account |
| http://localhost:8000/dashboard/ | User dashboard + watchlist |
| http://localhost:8000/stockbytop/ | Top gainers / trending / most active (login required) |

---

## Production deployment

```bash
cp .env.example .env
# Set: DJANGO_DEBUG=False, DJANGO_SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS

docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

App is served at **http://localhost:80** via Nginx. Static files are collected at container startup.

---

## Configuration

All variables are documented in [`.env.example`](.env.example). Main groups:

| Group | Variables |
|-------|-----------|
| Django | `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` |
| Database | `DB_*`, `POSTGRES_*` |
| Redis | `REDIS_URL`, `REDIS_CACHE_URL`, `CACHE_KEY_PREFIX` |
| Rate limiting | `RATE_LIMIT_ENABLED`, `RATE_LIMIT_API`, `RATE_LIMIT_HEAVY`, `RATE_LIMIT_WINDOW` |
| Screeners | `SCREENER_CACHE_TTL`, `SCREENER_REFRESH_INTERVAL` |
| Production | `GUNICORN_WORKERS`, `GUNICORN_TIMEOUT`, `HTTP_PORT` |

**Never commit `.env`** — it is gitignored. Commit `.env.example` only.

---

## Project structure

```
Taurus/
├── docker-compose.yml          # Development (runserver)
├── docker-compose.prod.yml     # Production (Gunicorn + Nginx)
├── Dockerfile
├── nginx/                      # Nginx config
├── scripts/                    # Production entrypoint
└── market-analyzer/
    ├── webapp/                 # Django settings, Celery, URLs
    ├── frontend_app/           # Views, templates, static assets, services
    ├── users/                  # Custom user model, auth, watchlist
    └── backend/                # Market data & analysis logic
        ├── datasources/        # Yahoo Finance integration
        ├── tecnical_analysis/  # TA metrics & patterns
        └── risk_manager/       # Fundamental scoring & signals
```

---

## Docker services (development)

| Service | Role |
|---------|------|
| `web` | Django dev server (port 8000) |
| `worker` | Celery worker |
| `beat` | Celery Beat (screener refresh every 15 min) |
| `db` | PostgreSQL |
| `redis` | Cache + Celery broker |

---

## Useful commands

```bash
# Run tests
docker compose exec web python manage.py test

# Django system check
docker compose exec web python manage.py check

# Refresh screeners manually
docker compose exec web python manage.py shell -c "
from frontend_app.services.screener_cache import refresh_all_screeners
print(refresh_all_screeners())
"

# Stop stack
docker compose down

# Reset database (destructive)
docker compose down -v
```

---

## Main API endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /stock/<symbol>/summary/` | Public | Aggregated page data + verdict + trade plan |
| `GET /stock/<symbol>/bio_info/` | Public | Company profile |
| `GET /stock/<symbol>/fundamental_*` | Public | Fundamentals, evaluations, charts |
| `GET /stock/<symbol>/crossover_trend/` | Public | EMA crossover (params: fast, medium, slow) |
| `GET /stockbytop/stock_gainers/` | Login | Top gainers (cached) |
| `GET /watchlist/` | Login | User watchlist |
| `POST /watchlist/add/` | Login | Add symbol |
| `POST /watchlist/<symbol>/remove/` | Login | Remove symbol |

Public JSON endpoints are rate-limited per IP (see `.env.example`).

---

## Investment verdict

The verdict on each stock page combines:

| Component | Weight | Source |
|-----------|--------|--------|
| Fundamentals | 45% | Pillar score 0–10 |
| Technicals | 55% | EMA, Bollinger, RSI signals |
| Analysts | modifier | Yahoo `recommendationMean` |

Output: **Buy**, **Hold**, or **Sell** + confidence % + bullet reasons.

Implementation: `market-analyzer/frontend_app/services/decision_verdict.py`

Full documentation: [docs/DECISION_VERDICT.md](docs/DECISION_VERDICT.md)

---

## Trade plan

When the verdict is **Buy** or **Sell**, a trade plan is shown below the verdict banner.

| Field | Description |
|-------|-------------|
| Entry | Current price |
| Stop-loss | From pattern or Bollinger |
| TP1 / TP2 | Profit targets + R:R |
| Size hint | Illustrative shares @ $10k portfolio, 2% risk |

**Source priority:** harmonic pattern → candlestick pattern → Bollinger fallback.

Implementation: `market-analyzer/frontend_app/services/trade_plan.py`

Full documentation: [docs/TRADE_PLAN.md](docs/TRADE_PLAN.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/DECISION_VERDICT.md](docs/DECISION_VERDICT.md) | Verdict formula and fields |
| [docs/TRADE_PLAN.md](docs/TRADE_PLAN.md) | Trade plan logic and schema |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Services and request flow |

---

## Data sources & delays

| Data type | Source | Typical delay |
|-----------|--------|---------------|
| Stocks / ETFs | Yahoo Finance | 1–2 minutes |
| Fundamentals | Yahoo Finance | 15–30 min (cached) |
| Screeners | Yahoo Finance (scraped) | Refreshed every 15 min |
| Insiders (US) | SEC via Yahoo | Varies |

Crypto (Binance) and economic calendar modules exist in code but are **not yet exposed** in the UI.

---

## Feature status

### Implemented

- Stock search and analysis page
- Unified summary endpoint + verdict banner
- **Trade plan** — entry, stop, TP, R:R, trailing stop, user portfolio sizing
- **Services layer** — `stock_data`, `technical_metrics`; thin views
- Technical & fundamental analysis
- Candlestick + harmonic patterns
- User auth, dashboard, watchlist
- Stock-by-top screeners (authenticated)
- Redis caching, rate limiting, Celery screeners
- CI pipeline, production Docker stack
- Excel downloads for financial statements

### In progress / planned

- Pivot points
- News sentiment (NLP)
- Economic calendar UI
- Crypto endpoints
- Optimizer / backtest UI
- Sector & peer comparison
- Portfolio tracking

### Deferred (far future)

- Push / email notifications (not on the current roadmap)

---

## Candlestick patterns

The app detects 40+ TA-Lib candlestick patterns. Only patterns whose stop-loss was **not** hit are shown.

| Pattern | Classification | Candles |
|---------|----------------|---------|
| Doji, Hammer, Engulfing, … | Reversal | 3 |
| Spinning Top, Tasuki Gap, … | Continuation | 3–5 |
| Three White Soldiers, Morning Star, … | Complex | 5–7 |

### Relevance rules

- **Recency** — recent patterns weigh more
- **Volatility** — old patterns fade faster in volatile markets
- **Overlap** — contradictory patterns in range are discarded
- **Not a standalone buy signal** — patterns alone do not justify opening a position

---

## Testing & CI

Tests run via GitHub Actions on push/PR to `main` and `develop`:

1. Build Docker stack
2. `manage.py migrate`
3. `manage.py check`
4. `manage.py test`

Run locally:

```bash
docker compose exec web python manage.py test
```

---

## Troubleshooting

**`.env` missing** — run `cp .env.example .env`

**Port 8000 in use** — change the port mapping in `docker-compose.yml`

**Migration errors** — run `docker compose exec web python manage.py migrate`

**Stock-by-top empty on first visit** — wait for Celery Beat or force refresh (see commands above)

**Static files in production** — generated by `collectstatic` at startup; do not commit `staticfiles/`

**Chart.js console errors** — hard refresh (`Ctrl+Shift+R`) after pulling frontend changes

---

## Authors

Built with 💻 by [@joaomalho](https://github.com/joaomalho).

---

## License

See [LICENSE](LICENSE) in this repository.

---

## Community

- **Issues:** [GitHub Issues](https://github.com/joaomalho/Taurus/issues)
- **Discord:** [Join here](https://discord.gg/TnjNUGxr)

We welcome maintainers, testers, UI/UX designers, and market analysts.

---

## Recent improvements (2025–2026)

- **Trade plan** — entry, stop-loss, TP, R:R (Phase 2)
- **Services refactor** — views → stock_data + technical_metrics
- Unified `/summary/` endpoint (1 request instead of 11)
- Buy / Hold / Sell investment verdict
- User watchlist (dashboard + stock page)
- Celery Beat screener cache
- Rate limiting on public APIs
- Production stack (Gunicorn + Nginx)
- CI re-enabled with smoke tests
- Dashboard routing fix (`/dashboard/`)
- Server-side auth on stock-by-top
- Redis cache improvements for Yahoo data
- Bug fixes: Chart.js v4 theme, earnings API columns, toggle selectors
