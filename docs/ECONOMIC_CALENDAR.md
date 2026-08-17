# Economic calendar

Macro-economic release schedule for trading decisions.

## Data sources

| Source | When used |
|--------|-----------|
| **Forex Factory** (free) | Default — weekly feed via Fair Economy |
| **TradingEconomics** | When `TRADING_ECONOMICS_KEY` is set in `.env` |

The old TradingEconomics `guest:guest` account is discontinued.

## API

```
GET /economic-calendar/events/?timeframe=today
GET /economic-calendar/events/?timeframe=this%20week
GET /economic-calendar/events/?d1=2026-08-17&d2=2026-08-21
```

### Timeframes

- `today`, `yesterday`, `tomorrow`
- `this week`, `next week`

With the free feed, **next week** may return no events (notice shown in UI).

## UI

Page: `/economic-calendar/` — linked from the home page.

Grid columns: When, Country, Event, Impact, Forecast, Previous, Actual.

Impact badges: High (red), Medium (yellow), Low (green).

## Caching

Redis/Django cache — 5 minutes per timeframe (`CACHE_TTL_SECONDS` in service).

## Configuration

```env
# Optional — enables TradingEconomics instead of Forex Factory
TRADING_ECONOMICS_KEY=your_key:your_secret
```

## Implementation

| Layer | File |
|-------|------|
| Fetch + normalize | `backend/datasources/ecocalendar.py` |
| Cache + API | `frontend_app/services/economic_calendar.py` |
| Page + endpoint | `views.py`, `economiccalendar.html` |
| Frontend | `static/js/economic_calendar.js` |
