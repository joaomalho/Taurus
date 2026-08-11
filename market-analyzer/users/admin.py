from django.contrib import admin

from .models import User, WatchlistItem


@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "symbol", "created_at")
    search_fields = ("user__username", "symbol")
    ordering = ("-created_at",)


admin.site.register(User)
