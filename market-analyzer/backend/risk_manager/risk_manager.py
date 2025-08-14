import math
from backend.funcionalities.formulas import Formulas


class RiskManagerTechnical ():

    def __init__(self):
        self

    def relevance_candle(self):
        '''
        Determine whether the targets have already been reached following pattern detection, if not, consider them as active targets.
        Additionally, evaluate which pattern should be prioritized if multiple patterns are detected.
        '''

    def stoploss_manager():
        pass

    def take_profit_manager():
        pass

    def signal_decision_rsi(self, rsi_now, upper_level, lower_level):

        if rsi_now >= upper_level:
            rsi_signal = 'Sell'
        elif rsi_now <= lower_level:
            rsi_signal = 'Buy'
        else:
            rsi_signal = 'Flat'
        return rsi_signal

    def signal_decision_bbands(self, last_close, lower_band, upper_band):

        if last_close <= lower_band:
            bbands_signal = 'Buy'
        elif last_close >= upper_band:
            bbands_signal = 'Sell'
        else:
            bbands_signal = 'Flat'
        return bbands_signal

    def signal_decision_adx(self, adx_now):

        if adx_now < 20:
            adx_signal = 'Weak Trend'
        elif 20 <= adx_now < 50:
            adx_signal = 'Strong Trend'
        elif 50 <= adx_now < 75:
            adx_signal = 'Very Strong Trend'
        else:
            adx_signal = 'Extremely Strong Trend'
        return adx_signal

    def signal_decision_crossover(self, ema_low, ema_mid, ema_high):

        if ema_low > ema_mid > ema_high:
            crossover_signal = 'Buy'
        elif ema_low < ema_mid < ema_high:
            crossover_signal = 'Sell'
        else:
            crossover_signal = 'Flat'
        return crossover_signal

    def stoploss_candles_conditions(self, signal, stoploss, future_close_prices):
        """
        Verify if stoploss were hitted in candle patterns
        """
        if stoploss is None:
            return "N/A"

        if signal == -100:
            return "Hit Stoploss (Above)" if any(close > stoploss for close in future_close_prices) else "No Hit"

        if signal == 100:
            return "Hit Stoploss (Below)" if any(close < stoploss for close in future_close_prices) else "No Hit"

        return "N/A"


class RiskManagerFundamental():

    def __init__(self):
        self.stoploss = None
        self.takeprofit = None

    @staticmethod
    def evaluation_bucket(label: str) -> str:
        """
        Classify fundamental metrics evaluation in buckets:
        * verygood
        * good
        * neutral
        * bad
        * nodata
        """
        if not label:
            return "nodata"

        s = str(label).strip().lower()

        verygood = [
            "very low undervalued",
            "good",
            "very good coverage (greedy)",
            "Good - Efficient Costs Management",
            "Good - Efficient Costs Management",
            "Good - Highly Profitable and Eficient Profit Generate",
            "Good - Highly Efficient in Generating Profits",
            "Good - Consistent Growth in Equity Returns"
        ]
        good = [
            "low undervalued",
            "undervalued",
            "good coverage",
            "healthy",
            "Healthy - Healthy Margins Good Management",
            "Healthy - Healthy Operational Management",
            "Healthy - Healthy and Solid Management",
            "Good - Growing Profitability Over Time",
            "Healthy - Efficient and Solid Management"
        ]
        neutral = [
            "no data",
            "Indefinido",
            "neutral",
            "neutral valued",
            "Moderated - Potential but Need Improvements",
            ]
        bad = [
            "overvalued",
            "high overvalued",
            "bad coverage (cut)",
            "tight margin to debt",
            "Not Good - Declining or No Growth"
        ]
        verybad = [
            "very high overvalued",
            "no coverage",
            "not good",
            "Not Good - Short Margins or High Costs",
            "Not Good - High Operational Costs or Difficulties to Get Revenue",
            "Not Good - High Operational Costs or Operational Problems",
            "Not Good - Low Efficiency on Equity Use",
            "Not Good - No Growth or Negative Trend"
        ]

        if any(k.lower() in s for k in verygood):
            return "verygood"
        if any(k.lower() in s for k in good):
            return "good"
        if any(k.lower() in s for k in neutral):
            return "neutral"
        if any(k.lower() in s for k in bad):
            return "bad"
        if any(k.lower() in s for k in verybad):
            return "verybad"
        return "neutral"

    @staticmethod
    def bucket_color(bucket: str) -> str:
        """
        Atributes a color to each classification bucket
        """
        return {
            "verygood": "#1cf467",
            "good": "#0f8a3b",
            "neutral": "#6b7280",
            "bad": "#9b3232",
            "verybad": "#ff1414",
            "nodata": "#9E9E9E",
        }.get(bucket, "#6b7280")

    @staticmethod
    def _is_number(x):
        return isinstance(x, (int, float)) and not math.isnan(x)

    def _set_eval(self, out: dict, key: str, text: str):
        out[f"{key}_evaluation"] = text
        bucket = self.evaluation_bucket(text)
        out[f"{key}_bucket"] = bucket
        out[f"{key}_color"] = self.bucket_color(bucket)

    def evaluate_metrics(self, metrics):
        """
        Evaluate fundamental metrics.
        """

        fm = Formulas()

        evaluated_metrics = {}

        # Valuation
        valuation = metrics.get('valuation', {})
        trailing_pe = fm.safe_round(valuation.get("trailingPE"))
        sector_pe = fm.safe_round(valuation.get("sectorTrailingPE"))
        forward_pe = fm.safe_round(valuation.get("forwardPE"))

        # Guardar os valores convertidos
        evaluated_metrics["trailingPE"] = trailing_pe if trailing_pe is not None else None
        evaluated_metrics["sectorTrailingPE"] = sector_pe if sector_pe is not None else None
        evaluated_metrics["forwardPE"] = forward_pe if forward_pe is not None else None

        # Só avalia o score se TODOS estiverem presentes
        if None not in (trailing_pe, sector_pe, forward_pe):
            score_pe = 0
            score_pe += 1 if trailing_pe < sector_pe else -1 if trailing_pe > sector_pe else 0
            score_pe += 1 if forward_pe < sector_pe else -1 if forward_pe > sector_pe else 0
            score_pe += 1 if trailing_pe > forward_pe else -1 if trailing_pe < forward_pe else 0

            text_trailingPE = {
                3:  "Very Low Undervalued",
                2:  "Low Undervalued",
                1:  "Undervalued",
                0:  "Neutral Valued",
                -1: "Overvalued",
                -2: "High Overvalued",
            }.get(score_pe, "Very High Overvalued")
        else:
            text_trailingPE = "No Data"

        self._set_eval(evaluated_metrics, "trailingPE", text_trailingPE)

        # Valuation - PEG Ratio
        peg_raw = fm.safe_round(metrics.get('valuation', {}).get("PEGRatio"))

        evaluated_metrics["PEGRatio"] = peg_raw if peg_raw is not None else None

        if peg_raw is None:
            text_PEGRatio = "No Data"
        else:
            if peg_raw < 1:
                text_PEGRatio = "Undervalued"
            elif peg_raw == 1:
                text_PEGRatio = "Neutral Valued"
            else:
                text_PEGRatio = "Overvalued"

        self._set_eval(evaluated_metrics, "PEGRatio", text_PEGRatio)

        # Dividends - Dividend Coverage Ratio
        div_coverage_raw = fm.safe_round(metrics.get('dividends', {}).get("divCoverageRate"))

        # Armazenar o valor bruto
        evaluated_metrics["divCoverageRate"] = div_coverage_raw if div_coverage_raw is not None else None

        # Avaliação
        if div_coverage_raw is None:
            text_divCoverageRate = "No Data"
        else:
            if div_coverage_raw <= 1:
                text_divCoverageRate = "No Coverage"
            elif div_coverage_raw <= 1.5:
                text_divCoverageRate = "Bad Coverage (Cut)"
            elif div_coverage_raw <= 3:
                text_divCoverageRate = "Good Coverage"
            else:
                text_divCoverageRate = "Very Good Coverage (Greedy)"

        self._set_eval(evaluated_metrics, "divCoverageRate", text_divCoverageRate)

        # Profitability - Cost of Revenue CAGR
        cost_revenue_cagr = fm.safe_round(metrics.get('profitability', {}).get("CostOfRevenueCAGR"))

        # Armazenar o valor bruto
        evaluated_metrics["CostOfRevenueCAGR"] = cost_revenue_cagr if cost_revenue_cagr is not None else None

        # Avaliação
        if cost_revenue_cagr is None or math.isnan(cost_revenue_cagr):
            text_CostOfRevenueCAGR = "No Data"
        else:
            if cost_revenue_cagr <= 0:
                text_CostOfRevenueCAGR = "Good"
            else:
                text_CostOfRevenueCAGR = "Not Good"

        self._set_eval(evaluated_metrics, "CostOfRevenueCAGR", text_CostOfRevenueCAGR)

        total_revenue_cagr = fm.safe_round(metrics.get('profitability', {}).get("TotalRevenueCAGR"))
        evaluated_metrics["TotalRevenueCAGR"] = total_revenue_cagr if total_revenue_cagr is not None else None

        if total_revenue_cagr is None or math.isnan(total_revenue_cagr):
            text_TotalRevenueCAGR = "No Data"
        else:
            text_TotalRevenueCAGR = "Good" if total_revenue_cagr > 0 else "Not Good"

        self._set_eval(evaluated_metrics, "TotalRevenueCAGR", text_TotalRevenueCAGR)

        # Debt
        net_worth = fm.safe_round(metrics.get('liquidity', {}).get("NetWorth"))
        evaluated_metrics["NetWorth"] = net_worth if net_worth is not None else None

        if net_worth is None:
            text_NetWorth = "No Data"
        else:
            text_NetWorth = "Good" if net_worth > 0 else "Not Good (In Debt)"

        self._set_eval(evaluated_metrics, "NetWorth", text_NetWorth)

        # Short Term Debt Coverage
        short_debt_cov = fm.safe_round(metrics.get('liquidity', {}).get("ShortTermDebtCoverage"))
        evaluated_metrics["ShortTermDebtCoverage"] = short_debt_cov if short_debt_cov is not None else None

        if short_debt_cov is None:
            text_ShortTermDebtCoverage = "No Data"
        else:
            text_ShortTermDebtCoverage = "Good" if short_debt_cov > 0 else "Not Good (In Debt)"

        self._set_eval(evaluated_metrics, "ShortTermDebtCoverage", text_ShortTermDebtCoverage)

        # Long Term Debt Coverage
        long_debt_cov = fm.safe_round(metrics.get('liquidity', {}).get("LongTermDebtCoverage"))
        evaluated_metrics["LongTermDebtCoverage"] = long_debt_cov if long_debt_cov is not None else None

        if long_debt_cov is None:
            text_LongTermDebtCoverage = "No Data"
        else:
            text_LongTermDebtCoverage = "Good" if long_debt_cov > 0 else "Not Good (In Debt)"

        self._set_eval(evaluated_metrics, "LongTermDebtCoverage", text_LongTermDebtCoverage)

        # Assets Growth
        total_assets_cagr = fm.safe_round(metrics.get('liquidity', {}).get("TotalAssetsCAGR"))
        evaluated_metrics["TotalAssetsCAGR"] = total_assets_cagr if total_assets_cagr is not None else None

        if total_assets_cagr is None or math.isnan(total_assets_cagr):
            text_TotalAssetsCAGR = "No Data"
        else:
            text_TotalAssetsCAGR = "Good" if total_assets_cagr > 0 else "Not Good"

        self._set_eval(evaluated_metrics, "TotalAssetsCAGR", text_TotalAssetsCAGR)

        # Liabilities Growth
        total_liabilities_cagr = fm.safe_round(metrics.get('liquidity', {}).get("TotalLiabilitiesCAGR"))
        evaluated_metrics["TotalLiabilitiesCAGR"] = total_liabilities_cagr if total_liabilities_cagr is not None else None

        if total_liabilities_cagr is None or math.isnan(total_liabilities_cagr):
            text_TotalLiabilitiesCAGR = "No Data"
        else:
            text_TotalLiabilitiesCAGR = "Good" if total_liabilities_cagr <= 0 else "Not Good"

        self._set_eval(evaluated_metrics, "TotalLiabilitiesCAGR", text_TotalLiabilitiesCAGR)

        # Stockholders Equity
        stockholders_equity_cagr = fm.safe_round(metrics.get('liquidity', {}).get("StockholdersEquityCAGR"))
        evaluated_metrics["StockholdersEquityCAGR"] = stockholders_equity_cagr if stockholders_equity_cagr is not None else None

        if stockholders_equity_cagr is None or math.isnan(stockholders_equity_cagr):
            text_StockholdersEquityCAGR = "No Data"
        else:
            text_StockholdersEquityCAGR = "Good" if stockholders_equity_cagr > 0 else "Not Good"

        self._set_eval(evaluated_metrics, "StockholdersEquityCAGR", text_StockholdersEquityCAGR)

        # Cash
        # Free Cashflow Yield
        fcf_yield = fm.safe_round(metrics.get('cashflow', {}).get("FreeCashflowYield"))
        evaluated_metrics["FreeCashflowYield"] = fcf_yield if fcf_yield is not None else None

        if fcf_yield is None:
            text_FreeCashflowYield = "No Data"
        elif fcf_yield <= 2:
            text_FreeCashflowYield = "Overvalued / Bad to Generate Cash"
        elif fcf_yield <= 5:
            text_FreeCashflowYield = "Healthy / Consistent to Generates Cash"
        else:
            text_FreeCashflowYield = "Undervalued / Highly Profitable"

        self._set_eval(evaluated_metrics, "FreeCashflowYield", text_FreeCashflowYield)

        # Ratios
        # Current Ratio
        current_ratio = fm.safe_round(metrics.get('ratios', {}).get("CurrentRatio"))
        evaluated_metrics["CurrentRatio"] = current_ratio if current_ratio is not None else None

        if current_ratio is None:
            text_CurrentRatio = "No Data"
        else:
            if current_ratio <= 100:
                text_CurrentRatio = "Not Good (In Debt)"
            elif current_ratio <= 120:
                text_CurrentRatio = "Tight Margin to Debt"
            elif current_ratio <= 200:
                text_CurrentRatio = "Good Debt Coverage"
            else:
                text_CurrentRatio = "Perfect Coverage (Double +)"

        self._set_eval(evaluated_metrics, "CurrentRatio", text_CurrentRatio)

        # Current Ratio Growth
        current_ratio_cagr = fm.safe_round(metrics.get('ratios', {}).get("CurrentRatioCAGR"))
        evaluated_metrics["CurrentRatioCAGR"] = current_ratio_cagr if current_ratio_cagr is not None else None

        if current_ratio_cagr is None or math.isnan(current_ratio_cagr):
            text_CurrentRatioCAGR = "No Data"
        else:
            text_CurrentRatioCAGR = "Good" if current_ratio_cagr > 0 else "Not Good"

        self._set_eval(evaluated_metrics, "CurrentRatioCAGR", text_CurrentRatioCAGR)

        # Cash Ratio
        cash_ratio = fm.safe_round(metrics.get('ratios', {}).get("CashRatio"))
        evaluated_metrics["CashRatio"] = cash_ratio if cash_ratio is not None else None

        if cash_ratio is None:
            text_CashRatio = "No Data"
        else:
            if cash_ratio <= 50:
                text_CashRatio = "Not Good (In Debt)"
            elif cash_ratio <= 100:
                text_CashRatio = "Good Debt Coverage"
            else:
                text_CashRatio = "Good Debt Coverage (Too Conservative)"

        self._set_eval(evaluated_metrics, "CashRatio", text_CashRatio)

        # Current Ratio Growth
        cash_ratio_cagr = fm.safe_round(metrics.get('ratios', {}).get("CashRatioCAGR"))
        evaluated_metrics["CashRatioCAGR"] = cash_ratio_cagr if cash_ratio_cagr is not None else None

        if cash_ratio_cagr is None or math.isnan(cash_ratio_cagr):
            text_CashRatioCAGR = "No Data"
        else:
            if cash_ratio_cagr <= 0:
                text_CashRatioCAGR = "Not Good"
            else:
                text_CashRatioCAGR = "Good"

        self._set_eval(evaluated_metrics, "CashRatioCAGR", text_CashRatioCAGR)

        # Gross Margin
        gross_margin = fm.safe_round(metrics.get('ratios', {}).get("GrossMargin"))
        evaluated_metrics["GrossMargin"] = gross_margin if gross_margin is not None else None

        if gross_margin is None:
            text_GrossMargin = "No Data"
        else:
            if gross_margin <= 25:
                text_GrossMargin = "Not Good - Short Margins or High Costs"
            elif gross_margin <= 40:
                text_GrossMargin = "Healthy - Healthy Margins Good Management"
            else:
                text_GrossMargin = "Good - Efficient Costs Management"

        self._set_eval(evaluated_metrics, "GrossMargin", text_GrossMargin)

        # Gross Margin Growth
        gross_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("GrossMarginCAGR"))
        evaluated_metrics["GrossMarginCAGR"] = gross_margin_cagr if gross_margin_cagr is not None else None

        if gross_margin_cagr is None or math.isnan(gross_margin_cagr):
            text_GrossMarginCAGR = "No Data"
        else:
            text_GrossMarginCAGR = (
                "Good" if gross_margin_cagr > 0 else "Not Good"
            )

        self._set_eval(evaluated_metrics, "GrossMarginCAGR", text_GrossMarginCAGR)

        # Operating Margin
        operating_margin = fm.safe_round(metrics.get('ratios', {}).get("OperatingMargin"))
        evaluated_metrics["OperatingMargin"] = operating_margin if operating_margin is not None else None

        if operating_margin is None:
            text_OperatingMargin = "No Data"
        else:
            if operating_margin <= 10:
                text_OperatingMargin = "Not Good - High Operational Costs or Difficulties to Get Revenue"
            elif operating_margin <= 20:
                text_OperatingMargin = "Healthy - Healthy Operational Management"
            else:
                text_OperatingMargin = "Good - Efficient Costs Management"

        self._set_eval(evaluated_metrics, "OperatingMargin", text_OperatingMargin)

        # Operational Margin Growth
        operating_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("OperatingMarginCAGR"))
        evaluated_metrics["OperatingMarginCAGR"] = operating_margin_cagr if operating_margin_cagr is not None else None

        if operating_margin_cagr is None or math.isnan(operating_margin_cagr):
            text_OperatingMarginCAGR = "No Data"
        else:
            if operating_margin_cagr <= 0:
                text_OperatingMarginCAGR = "Not Good"
            else:
                text_OperatingMarginCAGR = "Good"

        self._set_eval(evaluated_metrics, "OperatingMarginCAGR", text_OperatingMarginCAGR)

        # Profit Margin
        profit_margin = fm.safe_round(metrics.get('ratios', {}).get("ProfitMargin"))
        evaluated_metrics["ProfitMargin"] = profit_margin if profit_margin is not None else None

        if profit_margin is None:
            text_ProfitMargin = "No Data"
        else:
            if profit_margin <= 5:
                text_ProfitMargin = "Not Good - High Operational Costs or Operational Problems"
            elif profit_margin <= 10:
                text_ProfitMargin = "Moderated - Potential but Need Improvements"
            elif profit_margin <= 20:
                text_ProfitMargin = "Healthy - Healthy and Solid Management"
            else:
                text_ProfitMargin = "Good - Highly Profitable and Eficient Profit Generate"

        self._set_eval(evaluated_metrics, "ProfitMargin", text_ProfitMargin)

        # Profit Margin Growth
        profit_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("ProfitMarginCAGR"))
        evaluated_metrics["ProfitMarginCAGR"] = profit_margin_cagr if profit_margin_cagr is not None else None

        if profit_margin_cagr is None or math.isnan(profit_margin_cagr):
            text_ProfitMarginCAGR = "No Data"
        else:
            if profit_margin_cagr <= 0:
                text_ProfitMarginCAGR = "Not Good - Declining or No Growth"
            else:
                text_ProfitMarginCAGR = "Good - Growing Profitability Over Time"

        self._set_eval(evaluated_metrics, "ProfitMarginCAGR", text_ProfitMarginCAGR)

        # Return On Equity
        return_on_equity = fm.safe_round(metrics.get('ratios', {}).get("ReturnOnEquity"))
        evaluated_metrics["ReturnOnEquity"] = return_on_equity if return_on_equity is not None else None

        if return_on_equity is None:
            text_ReturnOnEquity = "No Data"
        else:
            if return_on_equity <= 10:
                text_ReturnOnEquity = "Not Good - Low Efficiency on Equity Use"
            elif return_on_equity <= 15:
                text_ReturnOnEquity = "Moderated - Potential but Need Improvements"
            elif return_on_equity <= 20:
                text_ReturnOnEquity = "Healthy - Efficient and Solid Management"
            else:
                text_ReturnOnEquity = "Good - Highly Efficient in Generating Profits"

        self._set_eval(evaluated_metrics, "ReturnOnEquity", text_ReturnOnEquity)

        # Return On Equity Growth
        return_on_equity_cagr = fm.safe_round(metrics.get('ratios', {}).get("ReturnOnEquityCAGR"))
        evaluated_metrics["ReturnOnEquityCAGR"] = return_on_equity_cagr if return_on_equity_cagr is not None else None

        if return_on_equity_cagr is None or math.isnan(return_on_equity_cagr):
            text_ReturnOnEquityCAGR = "No Data"
        else:
            if return_on_equity_cagr <= 0:
                text_ReturnOnEquityCAGR = "Not Good - No Growth or Negative Trend"
            else:
                text_ReturnOnEquityCAGR = "Good - Consistent Growth in Equity Returns"

        self._set_eval(evaluated_metrics, "ReturnOnEquityCAGR", text_ReturnOnEquityCAGR)

        return evaluated_metrics if evaluated_metrics else "Indefinido"
