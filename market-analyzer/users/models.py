from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import normalize_symbol

MAX_WATCHLIST_ITEMS = 50
MAX_PORTFOLIO_POSITIONS = 50
DEFAULT_PORTFOLIO_VALUE = 10_000
DEFAULT_RISK_PERCENT = 2.0


class User(AbstractUser):
    display_name = models.CharField(max_length=150, blank=True)
    portfolio_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=DEFAULT_PORTFOLIO_VALUE,
        validators=[MinValueValidator(100), MaxValueValidator(10_000_000)],
    )
    risk_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=DEFAULT_RISK_PERCENT,
        validators=[MinValueValidator(0.1), MaxValueValidator(10)],
    )


class WatchlistItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist_items",
    )
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "symbol"],
                name="unique_watchlist_symbol_per_user",
            )
        ]

    def save(self, *args, **kwargs):
        self.symbol = normalize_symbol(self.symbol)
        super().save(*args, **kwargs)

    @classmethod
    def add_symbol(cls, user, symbol: str) -> "WatchlistItem":
        symbol = normalize_symbol(symbol)
        if cls.objects.filter(user=user).count() >= MAX_WATCHLIST_ITEMS:
            raise ValidationError(f"Watchlist limit reached ({MAX_WATCHLIST_ITEMS} symbols).")
        item, created = cls.objects.get_or_create(user=user, symbol=symbol)
        if not created:
            raise ValidationError("Symbol already in watchlist.")
        return item

    @classmethod
    def remove_symbol(cls, user, symbol: str) -> bool:
        symbol = normalize_symbol(symbol)
        deleted, _ = cls.objects.filter(user=user, symbol=symbol).delete()
        return deleted > 0


class PortfolioPosition(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="portfolio_positions",
    )
    symbol = models.CharField(max_length=10)
    shares = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        validators=[MinValueValidator(0.0001)],
    )
    avg_cost = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0001)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "symbol"],
                name="unique_portfolio_symbol_per_user",
            )
        ]

    def save(self, *args, **kwargs):
        self.symbol = normalize_symbol(self.symbol)
        super().save(*args, **kwargs)

    @classmethod
    def upsert_position(
        cls,
        user,
        symbol: str,
        *,
        shares,
        avg_cost=None,
    ) -> "PortfolioPosition":
        symbol = normalize_symbol(symbol)
        if cls.objects.filter(user=user).exclude(symbol=symbol).count() >= MAX_PORTFOLIO_POSITIONS:
            raise ValidationError(f"Portfolio limit reached ({MAX_PORTFOLIO_POSITIONS} positions).")

        position, _ = cls.objects.update_or_create(
            user=user,
            symbol=symbol,
            defaults={"shares": shares, "avg_cost": avg_cost},
        )
        return position

    @classmethod
    def remove_position(cls, user, symbol: str) -> bool:
        symbol = normalize_symbol(symbol)
        deleted, _ = cls.objects.filter(user=user, symbol=symbol).delete()
        return deleted > 0

