from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from users.models import MAX_WATCHLIST_ITEMS, MAX_PORTFOLIO_POSITIONS, PortfolioPosition, WatchlistItem

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


class PortfolioModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="portuser", password="pass12345")

    def test_upsert_and_remove_position(self):
        position = PortfolioPosition.upsert_position(
            self.user,
            "aapl",
            shares="10",
            avg_cost="150",
        )
        self.assertEqual(position.symbol, "AAPL")
        self.assertTrue(PortfolioPosition.objects.filter(user=self.user, symbol="AAPL").exists())
        self.assertTrue(PortfolioPosition.remove_position(self.user, "AAPL"))
        self.assertFalse(PortfolioPosition.objects.filter(user=self.user, symbol="AAPL").exists())

    def test_upsert_updates_existing_position(self):
        PortfolioPosition.upsert_position(self.user, "MSFT", shares="5", avg_cost="300")
        position = PortfolioPosition.upsert_position(self.user, "MSFT", shares="8", avg_cost="310")
        self.assertEqual(float(position.shares), 8.0)
        self.assertEqual(PortfolioPosition.objects.filter(user=self.user).count(), 1)

    def test_portfolio_limit(self):
        for i in range(MAX_PORTFOLIO_POSITIONS):
            PortfolioPosition.upsert_position(self.user, f"S{i}", shares="1")
        with self.assertRaises(ValidationError):
            PortfolioPosition.upsert_position(self.user, "FULL", shares="1")


class PortfolioAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="portapi", password="pass12345")
        self.client = Client()
        self.client.login(username="portapi", password="pass12345")

    def test_list_requires_login(self):
        client = Client()
        response = client.get(reverse("portfolio_list"))
        self.assertEqual(response.status_code, 401)

    @patch("frontend_app.services.portfolio.stock_data.fetch_bio")
    def test_upsert_list_and_remove_position(self, mock_bio):
        mock_bio.return_value = {
            "data": {
                "LongName": "Apple Inc.",
                "CurrentPrice": 180,
            }
        }

        response = self.client.post(
            reverse("portfolio_upsert"),
            data='{"symbol":"AAPL","shares":10,"avg_cost":150}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["symbol"], "AAPL")

        response = self.client.get(reverse("portfolio_list"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["totals"]["position_count"], 1)
        self.assertEqual(payload["positions"][0]["symbol"], "AAPL")
        self.assertEqual(payload["positions"][0]["market_value"], 1800.0)

        response = self.client.post(reverse("portfolio_remove", kwargs={"symbol": "AAPL"}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["removed"])

        response = self.client.get(reverse("portfolio_list"))
        self.assertEqual(response.json()["totals"]["position_count"], 0)

    def test_upsert_rejects_invalid_shares(self):
        response = self.client.post(
            reverse("portfolio_upsert"),
            data='{"symbol":"AAPL","shares":0}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
