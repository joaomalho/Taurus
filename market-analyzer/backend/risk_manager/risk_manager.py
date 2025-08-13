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

            evaluated_metrics["trailingPE_evaluation"] = {
                3:  "Very Low Undervalued",
                2:  "Low Undervalued",
                1:  "Undervalued",
                0:  "Neutral Valued",
                -1: "Overvalued",
                -2: "High Overvalued",
            }.get(score_pe, "Very High Overvalued")
        else:
            evaluated_metrics["trailingPE_evaluation"] = "No Data"

        # Valuation - PEG Ratio
        peg_raw = fm.safe_round(metrics.get('valuation', {}).get("PEGRatio"))

        evaluated_metrics["PEGRatio"] = peg_raw if peg_raw is not None else None

        if peg_raw is None:
            evaluated_metrics["PEGRatio_evaluation"] = "No Data"
        else:
            if peg_raw < 1:
                evaluated_metrics["PEGRatio_evaluation"] = "Undervalued"
            elif peg_raw == 1:
                evaluated_metrics["PEGRatio_evaluation"] = "Neutral Valued"
            else:
                evaluated_metrics["PEGRatio_evaluation"] = "Overvalued"

        # Dividends - Dividend Coverage Ratio
        div_coverage_raw = fm.safe_round(metrics.get('dividends', {}).get("divCoverageRate"))

        # Armazenar o valor bruto
        evaluated_metrics["divCoverageRate"] = div_coverage_raw if div_coverage_raw is not None else None

        # Avaliação
        if div_coverage_raw is None:
            evaluated_metrics["divCoverageRate_evaluation"] = "No Data"
        else:
            if div_coverage_raw <= 1:
                evaluated_metrics["divCoverageRate_evaluation"] = "No Coverage"
            elif div_coverage_raw <= 1.5:
                evaluated_metrics["divCoverageRate_evaluation"] = "Bad Coverage (Cut)"
            elif div_coverage_raw <= 3:
                evaluated_metrics["divCoverageRate_evaluation"] = "Good Coverage"
            else:
                evaluated_metrics["divCoverageRate_evaluation"] = "Very Good Coverage (Greedy)"

        # Profitability - Cost of Revenue CAGR
        cost_revenue_cagr = fm.safe_round(metrics.get('profitability', {}).get("CostOfRevenueCAGR"))

        # Armazenar o valor bruto
        evaluated_metrics["CostOfRevenueCAGR"] = cost_revenue_cagr if cost_revenue_cagr is not None else None

        # Avaliação
        if cost_revenue_cagr is None or math.isnan(cost_revenue_cagr):
            evaluated_metrics["CostOfRevenueCAGR_evaluation"] = "No Data"
        else:
            if cost_revenue_cagr <= 0:
                evaluated_metrics["CostOfRevenueCAGR_evaluation"] = "Good"
            else:
                evaluated_metrics["CostOfRevenueCAGR_evaluation"] = "Not Good"

        total_revenue_cagr = fm.safe_round(metrics.get('profitability', {}).get("TotalRevenueCAGR"))
        evaluated_metrics["TotalRevenueCAGR"] = total_revenue_cagr if total_revenue_cagr is not None else None

        if total_revenue_cagr is None or math.isnan(total_revenue_cagr):
            evaluated_metrics["TotalRevenueCAGR_evaluation"] = "No Data"
        else:
            evaluated_metrics["TotalRevenueCAGR_evaluation"] = "Good" if total_revenue_cagr > 0 else "Not Good"

        # Debt
        net_worth = fm.safe_round(metrics.get('liquidity', {}).get("NetWorth"))
        evaluated_metrics["NetWorth"] = net_worth if net_worth is not None else None

        if net_worth is None:
            evaluated_metrics["NetWorth_evaluation"] = "No Data"
        else:
            evaluated_metrics["NetWorth_evaluation"] = "Good" if net_worth > 0 else "Not Good (In Debt)"

        # Short Term Debt Coverage
        short_debt_cov = fm.safe_round(metrics.get('liquidity', {}).get("ShortTermDebtCoverage"))
        evaluated_metrics["ShortTermDebtCoverage"] = short_debt_cov if short_debt_cov is not None else None

        if short_debt_cov is None:
            evaluated_metrics["ShortTermDebtCoverage_evaluation"] = "No Data"
        else:
            evaluated_metrics["ShortTermDebtCoverage_evaluation"] = "Good" if short_debt_cov > 0 else "Not Good (In Debt)"

        # Long Term Debt Coverage
        long_debt_cov = fm.safe_round(metrics.get('liquidity', {}).get("LongTermDebtCoverage"))
        evaluated_metrics["LongTermDebtCoverage"] = long_debt_cov if long_debt_cov is not None else None

        if long_debt_cov is None:
            evaluated_metrics["LongTermDebtCoverage_evaluation"] = "No Data"
        else:
            evaluated_metrics["LongTermDebtCoverage_evaluation"] = "Good" if long_debt_cov > 0 else "Not Good (In Debt)"

        # Assets Growth
        total_assets_cagr = fm.safe_round(metrics.get('liquidity', {}).get("TotalAssetsCAGR"))
        evaluated_metrics["TotalAssetsCAGR"] = total_assets_cagr if total_assets_cagr is not None else None

        if total_assets_cagr is None or math.isnan(total_assets_cagr):
            evaluated_metrics["TotalAssetsCAGR_evaluation"] = "No Data"
        else:
            evaluated_metrics["TotalAssetsCAGR_evaluation"] = "Good" if total_assets_cagr > 0 else "Not Good"

        # Liabilities Growth
        total_liabilities_cagr = fm.safe_round(metrics.get('liquidity', {}).get("TotalLiabilitiesCAGR"))
        evaluated_metrics["TotalLiabilitiesCAGR"] = total_liabilities_cagr if total_liabilities_cagr is not None else None

        if total_liabilities_cagr is None or math.isnan(total_liabilities_cagr):
            evaluated_metrics["TotalLiabilitiesCAGR_evaluation"] = "No Data"
        else:
            evaluated_metrics["TotalLiabilitiesCAGR_evaluation"] = "Good" if total_liabilities_cagr <= 0 else "Not Good"

        # Stockholders Equity
        stockholders_equity_cagr = fm.safe_round(metrics.get('liquidity', {}).get("StockholdersEquityCAGR"))
        evaluated_metrics["StockholdersEquityCAGR"] = stockholders_equity_cagr if stockholders_equity_cagr is not None else None

        if stockholders_equity_cagr is None or math.isnan(stockholders_equity_cagr):
            evaluated_metrics["StockholdersEquityCAGR_evaluation"] = "No Data"
        else:
            evaluated_metrics["StockholdersEquityCAGR_evaluation"] = "Good" if stockholders_equity_cagr > 0 else "Not Good"

        # Cash
            # Free Cashflow Yield
        fcf_yield = fm.safe_round(metrics.get('cashflow', {}).get("FreeCashflowYield"))
        evaluated_metrics["FreeCashflowYield"] = fcf_yield if fcf_yield is not None else None

        if fcf_yield is None:
            evaluated_metrics["FreeCashflowYield_evaluation"] = "No Data"
        elif fcf_yield <= 2:
            evaluated_metrics["FreeCashflowYield_evaluation"] = "Overvalued / Bad to Generate Cash"
        elif fcf_yield <= 5:
            evaluated_metrics["FreeCashflowYield_evaluation"] = "Healthy / Consistent to Generates Cash"
        else:
            evaluated_metrics["FreeCashflowYield_evaluation"] = "Undervalued / Highly Profitable"

        # Ratios
            # Current Ratio
        current_ratio = fm.safe_round(metrics.get('ratios', {}).get("CurrentRatio"))
        evaluated_metrics["CurrentRatio"] = current_ratio if current_ratio is not None else None

        if current_ratio is None:
            evaluated_metrics["CurrentRatio_evaluation"] = "No Data"
        else:
            if current_ratio <= 100:
                evaluated_metrics["CurrentRatio_evaluation"] = "Not Good (In Debt)"
            elif current_ratio <= 120:
                evaluated_metrics["CurrentRatio_evaluation"] = "Tight Margin to Debt"
            elif current_ratio <= 200:
                evaluated_metrics["CurrentRatio_evaluation"] = "Good Debt Coverage"
            else:
                evaluated_metrics["CurrentRatio_evaluation"] = "Perfect Coverage (Double +)"

            # Current Ratio Growth
        current_ratio_cagr = fm.safe_round(metrics.get('ratios', {}).get("CurrentRatioCAGR"))
        evaluated_metrics["CurrentRatioCAGR"] = current_ratio_cagr if current_ratio_cagr is not None else None

        if current_ratio_cagr is None or math.isnan(current_ratio_cagr):
            evaluated_metrics["CurrentRatioCAGR_evaluation"] = "No Data"
        else:
            evaluated_metrics["CurrentRatioCAGR_evaluation"] = "Good" if current_ratio_cagr > 0 else "Not Good"

            # Cash Ratio
        cash_ratio = fm.safe_round(metrics.get('ratios', {}).get("CashRatio"))
        evaluated_metrics["CashRatio"] = cash_ratio if cash_ratio is not None else None

        if cash_ratio is None:
            evaluated_metrics["CashRatio_evaluation"] = "No Data"
        else:
            if cash_ratio <= 50:
                evaluated_metrics["CashRatio_evaluation"] = "Not Good (In Debt)"
            elif cash_ratio <= 100:
                evaluated_metrics["CashRatio_evaluation"] = "Good Debt Coverage"
            else:
                evaluated_metrics["CashRatio_evaluation"] = "Good Debt Coverage (Too Conservative)"

            # Current Ratio Growth
        cash_ratio_cagr = fm.safe_round(metrics.get('ratios', {}).get("CashRatioCAGR"))
        evaluated_metrics["CashRatioCAGR"] = cash_ratio_cagr if cash_ratio_cagr is not None else None

        if cash_ratio_cagr is None or math.isnan(cash_ratio_cagr):
            evaluated_metrics["CashRatioCAGR_evaluation"] = "No Data"
        else:
            if cash_ratio_cagr <= 0:
                evaluated_metrics["CashRatioCAGR_evaluation"] = "Not Good"
            else:
                evaluated_metrics["CashRatioCAGR_evaluation"] = "Good"

            # Gross Margin
        gross_margin = fm.safe_round(metrics.get('ratios', {}).get("GrossMargin"))
        evaluated_metrics["GrossMargin"] = gross_margin if gross_margin is not None else None

        if gross_margin is None:
            evaluated_metrics["GrossMargin_evaluation"] = "No Data"
        else:
            if gross_margin <= 25:
                evaluated_metrics["GrossMargin_evaluation"] = "Not Good - Short Margins or High Costs"
            elif gross_margin <= 40:
                evaluated_metrics["GrossMargin_evaluation"] = "Healthy - Healthy Margins Good Management"
            else:
                evaluated_metrics["GrossMargin_evaluation"] = "Good - Efficient Costs Management"

            # Gross Margin Growth
        gross_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("GrossMarginCAGR"))
        evaluated_metrics["GrossMarginCAGR"] = gross_margin_cagr if gross_margin_cagr is not None else None

        if gross_margin_cagr is None or math.isnan(gross_margin_cagr):
            evaluated_metrics["GrossMarginCAGR_evaluation"] = "No Data"
        else:
            evaluated_metrics["GrossMarginCAGR_evaluation"] = (
                "Good" if gross_margin_cagr > 0 else "Not Good"
            )

            # Operating Margin
        operating_margin = fm.safe_round(metrics.get('ratios', {}).get("OperatingMargin"))
        evaluated_metrics["OperatingMargin"] = operating_margin if operating_margin is not None else None

        if operating_margin is None:
            evaluated_metrics["OperatingMargin_evaluation"] = "No Data"
        else:
            if operating_margin <= 10:
                evaluated_metrics["OperatingMargin_evaluation"] = "Not Good - High Operational Costs or Difficulties to Get Revenue"
            elif operating_margin <= 20:
                evaluated_metrics["OperatingMargin_evaluation"] = "Healthy - Healthy Operational Management"
            else:
                evaluated_metrics["OperatingMargin_evaluation"] = "Good - Efficient Cost Management"

            # Operational Margin Growth
        operating_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("OperatingMarginCAGR"))
        evaluated_metrics["OperatingMarginCAGR"] = operating_margin_cagr if operating_margin_cagr is not None else None

        if operating_margin_cagr is None or math.isnan(operating_margin_cagr):
            evaluated_metrics["OperatingMarginCAGR_evaluation"] = "No Data"
        else:
            if operating_margin_cagr <= 0:
                evaluated_metrics["OperatingMarginCAGR_evaluation"] = "Not Good"
            else:
                evaluated_metrics["OperatingMarginCAGR_evaluation"] = "Good"

            # Profit Margin
        profit_margin = fm.safe_round(metrics.get('ratios', {}).get("ProfitMargin"))
        evaluated_metrics["ProfitMargin"] = profit_margin if profit_margin is not None else None

        if profit_margin is None:
            evaluated_metrics["ProfitMargin_evaluation"] = "No Data"
        else:
            if profit_margin <= 5:
                evaluated_metrics["ProfitMargin_evaluation"] = "Not Good - High Operational Costs or Operational Problems"
            elif profit_margin <= 10:
                evaluated_metrics["ProfitMargin_evaluation"] = "Moderated - Potential but Need Improvements"
            elif profit_margin <= 20:
                evaluated_metrics["ProfitMargin_evaluation"] = "Healthy - Healthy and Solid Management"
            else:
                evaluated_metrics["ProfitMargin_evaluation"] = "Good - Highly Profitable and Eficient Profit Generate"

            # Profit Margin Growth
        profit_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("ProfitMarginCAGR"))
        evaluated_metrics["ProfitMarginCAGR"] = profit_margin_cagr if profit_margin_cagr is not None else None

        if profit_margin_cagr is None or math.isnan(profit_margin_cagr):
            evaluated_metrics["ProfitMarginCAGR_evaluation"] = "No Data"
        else:
            if profit_margin_cagr <= 0:
                evaluated_metrics["ProfitMarginCAGR_evaluation"] = "Not Good - Declining or No Growth"
            else:
                evaluated_metrics["ProfitMarginCAGR_evaluation"] = "Good - Growing Profitability Over Time"

            # Return On Equity
        return_on_equity = fm.safe_round(metrics.get('ratios', {}).get("ReturnOnEquity"))
        evaluated_metrics["ReturnOnEquity"] = return_on_equity if return_on_equity is not None else None

        if return_on_equity is None:
            evaluated_metrics["ReturnOnEquity_evaluation"] = "No Data"
        else:
            if return_on_equity <= 10:
                evaluated_metrics["ReturnOnEquity_evaluation"] = "Not Good - Low Efficiency on Equity Use"
            elif return_on_equity <= 15:
                evaluated_metrics["ReturnOnEquity_evaluation"] = "Moderated - Potential but Needs Improvement"
            elif return_on_equity <= 20:
                evaluated_metrics["ReturnOnEquity_evaluation"] = "Healthy - Efficient and Solid Management"
            else:
                evaluated_metrics["ReturnOnEquity_evaluation"] = "Good - Highly Efficient in Generating Profits"

            # Return On Equity Growth
        return_on_equity_cagr = fm.safe_round(metrics.get('ratios', {}).get("ReturnOnEquityCAGR"))
        evaluated_metrics["ReturnOnEquityCAGR"] = return_on_equity_cagr if return_on_equity_cagr is not None else None

        if return_on_equity_cagr is None or math.isnan(return_on_equity_cagr):
            evaluated_metrics["ReturnOnEquityCAGR_evaluation"] = "No Data"
        else:
            if return_on_equity_cagr <= 0:
                evaluated_metrics["ReturnOnEquityCAGR_evaluation"] = "Not Good - No Growth or Negative Trend"
            else:
                evaluated_metrics["ReturnOnEquityCAGR_evaluation"] = "Good - Consistent Growth in Equity Returns"

        return evaluated_metrics if evaluated_metrics else "Indefinido"
