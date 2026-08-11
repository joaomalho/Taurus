from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .validators import normalize_symbol

MAX_WATCHLIST_ITEMS = 50


class User(AbstractUser):
    display_name = models.CharField(max_length=150, blank=True)


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

