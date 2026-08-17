from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from users.models import User


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class DashboardRoutingTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_dashboard_accessible_when_logged_in(self):
        User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_home_does_not_shadow_dashboard(self):
        """Home and dashboard must be distinct routes."""
        home = reverse("home")
        dashboard = reverse("dashboard")
        self.assertNotEqual(home, dashboard)
        self.assertEqual(dashboard, "/dashboard/")


class StockByTopAuthTests(TestCase):
    def test_stockbytop_page_requires_login(self):
        response = self.client.get(reverse("stockbytop_page"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_stockbytop_api_requires_login(self):
        for name in ("get_stock_gainers", "get_stock_trending", "get_stock_most_active"):
            with self.subTest(endpoint=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.json()["error"], "Authentication required")

    def test_stockbytop_page_accessible_when_logged_in(self):
        User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("stockbytop_page"))
        self.assertEqual(response.status_code, 200)


@override_settings(RATE_LIMIT_ENABLED=True, RATE_LIMIT_API=2, RATE_LIMIT_WINDOW=60)
class RateLimitTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_stock_api_returns_429_when_limit_exceeded(self):
        url = reverse("get_bio_info", kwargs={"symbol": "AAPL"})
        self.assertNotEqual(self.client.get(url).status_code, 429)
        self.assertNotEqual(self.client.get(url).status_code, 429)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json()["error"], "Rate limit exceeded. Try again later.")
        self.assertEqual(response["Retry-After"], "60")

    def test_stock_page_is_not_rate_limited(self):
        url = reverse("stock_page", kwargs={"symbol": "AAPL"})
        for _ in range(5):
            self.assertNotEqual(self.client.get(url).status_code, 429)

    def test_rate_limit_can_be_disabled(self):
        url = reverse("get_bio_info", kwargs={"symbol": "AAPL"})
        with self.settings(RATE_LIMIT_ENABLED=False, RATE_LIMIT_API=1):
            cache.clear()
            for _ in range(3):
                self.assertNotEqual(self.client.get(url).status_code, 429)


@override_settings(RATE_LIMIT_ENABLED=True, RATE_LIMIT_HEAVY=1, RATE_LIMIT_WINDOW=60)
class HeavyRateLimitTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_heavy_endpoint_has_stricter_limit(self):
        url = reverse("get_candle_detection", kwargs={"symbol": "AAPL"})
        self.assertNotEqual(self.client.get(url).status_code, 429)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 429)


@override_settings(RATE_LIMIT_ENABLED=False)
class StockSummaryTests(TestCase):
    @patch("frontend_app.views.build_stock_summary")
    def test_summary_endpoint_returns_payload(self, mock_build):
        mock_build.return_value = {
            "symbol": "AAPL",
            "bio": {"data": {"name": "Apple Inc."}},
            "news": {"data": []},
        }
        response = self.client.get(reverse("get_stock_summary", kwargs={"symbol": "AAPL"}))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["symbol"], "AAPL")
        self.assertIn("bio", payload)
        mock_build.assert_called_once_with("AAPL")

    def test_summary_rejects_invalid_symbol(self):
        response = self.client.get(reverse("get_stock_summary", kwargs={"symbol": "INVALID!"}))
        self.assertEqual(response.status_code, 404)


class DecisionVerdictTests(TestCase):
    def test_bullish_verdict_when_signals_align(self):
        from frontend_app.services.decision_verdict import build_decision_verdict

        result = build_decision_verdict(
            symbol="AAPL",
            fundamental_evaluations={
                "evaluations": {
                    "kpis": {
                        "trailingPE_bucket": "good",
                        "ROE_bucket": "verygood",
                        "ROA_bucket": "good",
                        "OperationalMargin_bucket": "good",
                        "FcfMargin_bucket": "good",
                        "CurrentRatio_bucket": "good",
                        "QuickRatio_bucket": "good",
                        "NetDebtEbitda_bucket": "good",
                        "GrowthReveneuYoY_bucket": "good",
                        "GrowthEPSYoY_bucket": "good",
                    }
                }
            },
            crossover={"signal": "Buy"},
            adx={"signal": "Strong Trend", "adx_now": 28},
            bollinger={"signal": "Buy"},
            rsi={"signal": "Flat"},
        )
        self.assertIn(result["verdict"], ("Buy", "Hold"))
        self.assertGreater(result["confidence"], 0)
        self.assertTrue(result["reasons"])

    def test_bearish_verdict_when_technicals_sell(self):
        from frontend_app.services.decision_verdict import build_decision_verdict

        result = build_decision_verdict(
            symbol="TEST",
            crossover={"signal": "Sell"},
            adx={"signal": "Strong Trend", "adx_now": 30},
            bollinger={"signal": "Sell"},
            rsi={"signal": "Sell"},
        )
        self.assertEqual(result["verdict"], "Sell")
        self.assertLess(result["score"], 0)


class TradePlanTests(TestCase):
    def test_hold_verdict_has_no_plan(self):
        from frontend_app.services.trade_plan import build_trade_plan

        plan = build_trade_plan(
            symbol="AAPL",
            verdict={"verdict": "Hold"},
            bio={"data": {"CurrentPrice": 100}},
        )
        self.assertFalse(plan["available"])
        self.assertIn("Hold", plan["reason"])

    def test_bollinger_fallback_for_buy(self):
        from frontend_app.services.trade_plan import build_trade_plan

        plan = build_trade_plan(
            symbol="AAPL",
            verdict={"verdict": "Buy"},
            bio={"data": {"CurrentPrice": 100}},
            bollinger={
                "lower_band": 95,
                "upper_band": 110,
                "signal": "Buy",
            },
        )
        self.assertTrue(plan["available"])
        self.assertEqual(plan["source"], "bollinger_fallback")
        self.assertEqual(plan["stop_loss"]["price"], 95)
        self.assertGreater(plan["targets"]["tp1"]["price"], 100)

    def test_harmonic_plan_preferred(self):
        from frontend_app.services.trade_plan import build_trade_plan

        plan = build_trade_plan(
            symbol="AAPL",
            verdict={"verdict": "Buy"},
            bio={"data": {"CurrentPrice": 182.5}},
            harmonic_patterns={
                "patterns_detected": [{
                    "pattern": "Gartley",
                    "direction": 1,
                    "stop_hit": False,
                    "STOP": 178.2,
                    "TP1": 188.0,
                    "TP2": 192.5,
                    "D_index": 120,
                }]
            },
            bollinger={"lower_band": 95, "upper_band": 110},
        )
        self.assertTrue(plan["available"])
        self.assertEqual(plan["source"], "harmonic_pattern")
        self.assertEqual(plan["entry"], 182.5)

    def test_custom_portfolio_changes_position_hint(self):
        from frontend_app.services.trade_plan import build_trade_plan

        plan = build_trade_plan(
            symbol="AAPL",
            verdict={"verdict": "Buy"},
            bio={"data": {"CurrentPrice": 100}},
            bollinger={"lower_band": 95, "upper_band": 110, "signal": "Buy"},
            portfolio_value=50_000,
            risk_percent=1.0,
        )
        self.assertTrue(plan["available"])
        self.assertEqual(plan["position_hint"]["portfolio_value"], 50_000)
        self.assertEqual(plan["position_hint"]["risk_percent"], 1.0)
        self.assertEqual(plan["position_hint"]["shares"], 100)

    def test_trailing_stop_included(self):
        from frontend_app.services.trade_plan import build_trade_plan

        plan = build_trade_plan(
            symbol="AAPL",
            verdict={"verdict": "Buy"},
            bio={"data": {"CurrentPrice": 100}},
            bollinger={"lower_band": 95, "upper_band": 110, "signal": "Buy"},
        )
        trail = plan["trailing_stop"]
        self.assertEqual(trail["activate_at"], plan["targets"]["tp1"]["price"])
        self.assertEqual(trail["move_stop_to"], 100)
        self.assertEqual(trail["trail_distance"], 5)


class TradingPrefsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="prefsuser", password="testpass123")

    def test_get_requires_login(self):
        response = self.client.get(reverse("trading_prefs"))
        self.assertEqual(response.status_code, 401)

    def test_get_returns_defaults_for_new_user(self):
        self.client.login(username="prefsuser", password="testpass123")
        response = self.client.get(reverse("trading_prefs"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["portfolio_value"], 10000)
        self.assertEqual(payload["risk_percent"], 2.0)

    def test_patch_updates_preferences(self):
        self.client.login(username="prefsuser", password="testpass123")
        response = self.client.patch(
            reverse("trading_prefs"),
            data='{"portfolio_value": 25000, "risk_percent": 1.5}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["portfolio_value"], 25000)
        self.assertEqual(payload["risk_percent"], 1.5)


class PivotPointsTests(TestCase):
    def test_classic_pivot_levels(self):
        from backend.tecnical_analysis.pivot_points import calculate_levels

        levels = calculate_levels(110, 90, 100, "classic")
        self.assertAlmostEqual(levels["pp"], 100.0)
        self.assertAlmostEqual(levels["r1"], 110.0)
        self.assertAlmostEqual(levels["s1"], 90.0)

    def test_fibonacci_pivot_levels(self):
        from backend.tecnical_analysis.pivot_points import calculate_levels

        levels = calculate_levels(110, 90, 100, "fibonacci")
        self.assertAlmostEqual(levels["pp"], 100.0)
        self.assertAlmostEqual(levels["r1"], 107.64, places=2)

    def test_compute_pivot_points_from_dataframe(self):
        import pandas as pd

        from frontend_app.services.technical_metrics import compute_pivot_points

        df = pd.DataFrame([
            {"Date": "2026-08-15", "Open": 98, "High": 110, "Low": 90, "Close": 100},
            {"Date": "2026-08-16", "Open": 101, "High": 105, "Low": 99, "Close": 104},
        ])
        result = compute_pivot_points("TEST", df, method="classic")
        self.assertEqual(result["symbol"], "TEST")
        self.assertIn("levels", result)
        self.assertIn(result["signal"], ("Buy", "Sell", "Flat"))

    @patch("frontend_app.views.technical_metrics.compute_pivot_points")
    def test_pivot_endpoint(self, mock_compute):
        mock_compute.return_value = {
            "symbol": "AAPL",
            "method": "classic",
            "levels": {"pp": 100},
            "signal": "Flat",
        }
        response = self.client.get(reverse("get_pivot_points", kwargs={"symbol": "AAPL"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["symbol"], "AAPL")


class ScreenerCacheTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch("frontend_app.services.screener_cache.dh.get_stocks_gainers")
    def test_refresh_screener_stores_data_in_cache(self, mock_gainers):
        import pandas as pd

        mock_gainers.return_value = pd.DataFrame([{"Symbol": "AAA", "Price": 1.0}])
        from frontend_app.services import screener_cache

        df = screener_cache.refresh_screener("gainers")
        self.assertEqual(len(df), 1)
        cached = screener_cache.get_screener("gainers")
        self.assertIsNotNone(cached)
        self.assertEqual(len(cached), 1)
        mock_gainers.assert_called_once()

    @patch("frontend_app.services.screener_cache.dh.get_stocks_gainers")
    def test_get_or_fetch_screener_uses_cache_without_refetch(self, mock_gainers):
        import pandas as pd

        from frontend_app.services import screener_cache

        screener_cache.set_screener("gainers", pd.DataFrame([{"Symbol": "BBB"}]))
        df = screener_cache.get_or_fetch_screener("gainers")
        self.assertEqual(len(df), 1)
        mock_gainers.assert_not_called()


@override_settings(
    RATE_LIMIT_ENABLED=False,
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
)
class ScreenerTaskTests(TestCase):
    @patch("frontend_app.tasks.refresh_all_screeners")
    def test_refresh_all_screeners_task(self, mock_refresh):
        mock_refresh.return_value = {"gainers": 100, "trending": 50, "most_active": 80}
        from frontend_app.tasks import refresh_all_screeners_task

        result = refresh_all_screeners_task.apply().get()
        self.assertEqual(result["gainers"], 100)
        mock_refresh.assert_called_once()
