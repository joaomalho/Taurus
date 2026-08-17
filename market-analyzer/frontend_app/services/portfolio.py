from decimal import Decimal, InvalidOperation

from frontend_app.services import stock_data
from users.models import PortfolioPosition


def _to_float(value) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
        if parsed != parsed:
            return None
        return parsed
    except (TypeError, ValueError):
        return None


def _serialize_position(position: PortfolioPosition) -> dict:
    bio = stock_data.fetch_bio(position.symbol)
    current_price = None
    company = position.symbol

    if isinstance(bio, dict) and "data" in bio:
        payload = bio["data"]
        current_price = _to_float(payload.get("CurrentPrice"))
        company = payload.get("LongName") or position.symbol

    shares = float(position.shares)
    avg_cost = float(position.avg_cost) if position.avg_cost is not None else None
    market_value = current_price * shares if current_price is not None else None
    cost_basis = avg_cost * shares if avg_cost is not None else None
    pnl = market_value - cost_basis if market_value is not None and cost_basis is not None else None
    pnl_pct = (pnl / cost_basis * 100) if pnl is not None and cost_basis else None

    return {
        "symbol": position.symbol,
        "company": company,
        "shares": shares,
        "avg_cost": avg_cost,
        "current_price": round(current_price, 4) if current_price is not None else None,
        "market_value": round(market_value, 2) if market_value is not None else None,
        "cost_basis": round(cost_basis, 2) if cost_basis is not None else None,
        "pnl": round(pnl, 2) if pnl is not None else None,
        "pnl_pct": round(pnl_pct, 2) if pnl_pct is not None else None,
        "updated_at": position.updated_at.isoformat(),
    }


def build_portfolio_summary(user) -> dict:
    positions = PortfolioPosition.objects.filter(user=user)
    rows = [_serialize_position(position) for position in positions]

    total_market = sum(row["market_value"] or 0 for row in rows)
    total_cost = sum(row["cost_basis"] or 0 for row in rows)
    priced_rows = [row for row in rows if row["market_value"] is not None]
    cost_rows = [row for row in rows if row["cost_basis"] is not None]

    total_pnl = None
    total_pnl_pct = None
    if cost_rows and all(row["cost_basis"] is not None for row in cost_rows):
        market_for_pnl = sum(row["market_value"] or 0 for row in cost_rows)
        total_pnl = market_for_pnl - total_cost
        total_pnl_pct = (total_pnl / total_cost * 100) if total_cost else None

    return {
        "positions": rows,
        "totals": {
            "market_value": round(total_market, 2) if priced_rows else None,
            "cost_basis": round(total_cost, 2) if cost_rows else None,
            "pnl": round(total_pnl, 2) if total_pnl is not None else None,
            "pnl_pct": round(total_pnl_pct, 2) if total_pnl_pct is not None else None,
            "position_count": len(rows),
        },
    }


def parse_shares(value) -> Decimal:
    try:
        shares = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Shares must be a positive number.")
    if shares <= 0:
        raise ValueError("Shares must be greater than zero.")
    return shares


def parse_avg_cost(value):
    if value is None or value == "":
        return None
    try:
        avg_cost = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Average cost must be a positive number.")
    if avg_cost <= 0:
        raise ValueError("Average cost must be greater than zero.")
    return avg_cost
