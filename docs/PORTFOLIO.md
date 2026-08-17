# Portfolio tracking

Track real holdings on the dashboard. Positions are stored per user and valued with the latest Yahoo price.

## Dashboard

Open `/dashboard/` (login required). The **Portfolio** card lets you:

- Add or update a position: symbol, shares, optional average cost
- View market value and P/L when average cost is set
- Remove positions

## API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/portfolio/` | Yes | List positions + totals |
| `POST` | `/portfolio/upsert/` | Yes | Create or update a position |
| `POST` | `/portfolio/<symbol>/remove/` | Yes | Remove a position |

### Upsert body

```json
{
  "symbol": "AAPL",
  "shares": 10,
  "avg_cost": 175.50
}
```

`avg_cost` is optional. Without it, the row shows shares and current price but no P/L.

### Limits

- Up to **50** positions per user
- Shares and average cost must be positive numbers

## Trade plan settings

**Portfolio value** and **risk per trade** on the same dashboard page are separate from holdings. They only feed position-sizing hints on stock pages (`/trading-prefs/`).
