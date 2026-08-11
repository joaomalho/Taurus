from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from users.models import MAX_WATCHLIST_ITEMS, WatchlistItem

User = get_user_model()


class WatchlistModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="watchuser", password="pass12345")

    def test_add_and_remove_symbol(self):
        item = WatchlistItem.add_symbol(self.user, "aapl")
        self.assertEqual(item.symbol, "AAPL")
        self.assertTrue(WatchlistItem.objects.filter(user=self.user, symbol="AAPL").exists())
        self.assertTrue(WatchlistItem.remove_symbol(self.user, "AAPL"))
        self.assertFalse(WatchlistItem.objects.filter(user=self.user, symbol="AAPL").exists())

    def test_duplicate_symbol_raises(self):
        WatchlistItem.add_symbol(self.user, "MSFT")
        with self.assertRaises(ValidationError):
            WatchlistItem.add_symbol(self.user, "MSFT")

    def test_invalid_symbol_raises(self):
        with self.assertRaises(ValidationError):
            WatchlistItem.add_symbol(self.user, "BAD!")

    def test_watchlist_limit(self):
        for i in range(MAX_WATCHLIST_ITEMS):
            WatchlistItem.add_symbol(self.user, f"S{i}")
        with self.assertRaises(ValidationError):
            WatchlistItem.add_symbol(self.user, "FULL")


class WatchlistAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="pass12345")
        self.client = Client()
        self.client.login(username="apiuser", password="pass12345")

    def test_list_requires_login(self):
        client = Client()
        response = client.get(reverse("watchlist_list"))
        self.assertEqual(response.status_code, 401)

    def test_add_list_and_remove_symbol(self):
        response = self.client.post(
            reverse("watchlist_add"),
            data='{"symbol":"AAPL"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["symbol"], "AAPL")

        response = self.client.get(reverse("watchlist_list"))
        self.assertEqual(response.status_code, 200)
        symbols = [item["symbol"] for item in response.json()["symbols"]]
        self.assertIn("AAPL", symbols)

        response = self.client.post(reverse("watchlist_remove", kwargs={"symbol": "AAPL"}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["removed"])

        response = self.client.get(reverse("watchlist_list"))
        symbols = [item["symbol"] for item in response.json()["symbols"]]
        self.assertNotIn("AAPL", symbols)

    def test_remove_missing_symbol_returns_404(self):
        response = self.client.post(reverse("watchlist_remove", kwargs={"symbol": "ZZZZ"}))
        self.assertEqual(response.status_code, 404)
