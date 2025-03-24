
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

        evaluated_metrics = {}

        # Valuation
        if "trailingPE" in metrics.get('valuation', {}) and "sectorTrailingPE" in metrics.get('valuation', {}) and "forwardPE" in metrics.get('valuation', {}):
            try:
                trailing_pe = round(float(metrics.get('valuation', {}).get("trailingPE", "N/A")), 2)
                sector_pe = round(float(metrics.get('valuation', {}).get("sectorTrailingPE", "N/A")), 2)
                forward_pe = round(float(metrics.get('valuation', {}).get("forwardPE", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["trailingPE"] = "N/A"
                return evaluated_metrics

            if not trailing_pe or not sector_pe or not forward_pe:
                evaluated_metrics["trailingPE"] = "N/A"
            else:
                score_pe = 0

                if trailing_pe < sector_pe:
                    score_pe += 1
                elif trailing_pe > sector_pe:
                    score_pe -= 1

                if forward_pe < sector_pe:
                    score_pe += 1
                elif forward_pe > sector_pe:
                    score_pe -= 1

                if trailing_pe > forward_pe:
                    score_pe += 1
                elif trailing_pe < forward_pe:
                    score_pe -= 1

                if score_pe >= 3:
                    evaluated_metrics["trailingPE"] = "Very Low Undervalued"
                elif score_pe == 2:
                    evaluated_metrics["trailingPE"] = "Low Undervalued"
                elif score_pe == 1:
                    evaluated_metrics["trailingPE"] = "Undervalued"
                elif score_pe == 0:
                    evaluated_metrics["trailingPE"] = "Neutral Valued"
                elif score_pe == -1:
                    evaluated_metrics["trailingPE"] = "Overvalued"
                elif score_pe == -2:
                    evaluated_metrics["trailingPE"] = "High Overvalued"
                else:
                    evaluated_metrics["trailingPE"] = "Very High Overvalued"

        if "PEGRatio" in metrics.get('valuation', {}):
            try:
                peg_ratio = round(float(metrics.get('valuation', {}).get("PEGRatio", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["PEGRatio"] = "N/A"
                return evaluated_metrics

            if not peg_ratio:
                evaluated_metrics["PEGRatio"] = "N/A"
            else:
                if peg_ratio < 1:
                    evaluated_metrics["PEGRatio"] = "Undervalued"
                elif peg_ratio == 1:
                    evaluated_metrics["PEGRatio"] = "Neutral Valued"
                else:
                    evaluated_metrics["PEGRatio"] = "Overvalued"

        # Dividends
        if "divCoverageRate" in metrics.get('dividends', {}):
            try:
                div_coverage_ratio = round(float(metrics.get('dividends', {}).get("divCoverageRate", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["divCoverageRate"] = "N/A"
                return evaluated_metrics
            
            if not div_coverage_ratio:
                evaluated_metrics["divCoverageRate"] = "N/A"
            else:
                if div_coverage_ratio <= 1:
                    evaluated_metrics["divCoverageRate"] = "No Coverage"
                elif div_coverage_ratio <= 1.5:
                    evaluated_metrics["divCoverageRate"] = "Bad Coverage (Cut)"
                elif div_coverage_ratio <= 3:
                    evaluated_metrics["divCoverageRate"] = "Good Coverage"
                else:
                    evaluated_metrics["divCoverageRate"] = "Very Good Coverage (Greedy)"
        
        # Profitability
        if "CostOfRevenueCAGR" in metrics.get('profitability', {}):
            try:
                cost_revenue_cagr = round(float(metrics.get('profitability', {}).get("CostOfRevenueCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["CostOfRevenueCAGR"] = "N/A"
                return evaluated_metrics
            
            if not cost_revenue_cagr:
                evaluated_metrics["CostOfRevenueCAGR"] = "N/A"
            else:
                if cost_revenue_cagr <= 0:
                    evaluated_metrics["CostOfRevenueCAGR"] = "Good"
                else:
                    evaluated_metrics["CostOfRevenueCAGR"] = "Not Good"

        if "TotalRevenueCAGR" in metrics.get('profitability', {}):
            try:
                total_revenue_cagr = round(float(metrics.get('profitability', {}).get("TotalRevenueCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["TotalRevenueCAGR"] = "N/A"
                return evaluated_metrics
            
            if not total_revenue_cagr:
                evaluated_metrics["TotalRevenueCAGR"] = "N/A"
            else:
                if total_revenue_cagr <= 0:
                    evaluated_metrics["TotalRevenueCAGR"] = "Not Good"
                else:
                    evaluated_metrics["TotalRevenueCAGR"] = "Good"

        # Debt
        if "NetWorth" in metrics.get('liquidity', {}):
            try:
                net_worth = round(float(metrics.get('liquidity', {}).get("NetWorth", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["NetWorth"] = "N/A"
                return evaluated_metrics
            
            if not net_worth:
                evaluated_metrics["NetWorth"] = "N/A"
            else:
                if net_worth <= 0:
                    evaluated_metrics["NetWorth"] = "Not Good (In Debt)"
                else:
                    evaluated_metrics["NetWorth"] = "Good"

            # Short Term Debt Coverage 
        if "ShortTermDebtCoverage" in metrics.get('liquidity', {}):
            try:
                short_debt_cov = round(float(metrics.get('liquidity', {}).get("ShortTermDebtCoverage", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["ShortTermDebtCoverage"] = "N/A"
                return evaluated_metrics
            
            if not short_debt_cov:
                evaluated_metrics["ShortTermDebtCoverage"] = "N/A"
            else:
                if short_debt_cov <= 0:
                    evaluated_metrics["ShortTermDebtCoverage"] = "Not Good (In Debt)"
                else:
                    evaluated_metrics["ShortTermDebtCoverage"] = "Good"
    
            # Long Term Debt Coverage 
        if "LongTermDebtCoverage" in metrics.get('liquidity', {}):
            try:
                long_debt_cov = round(float(metrics.get('liquidity', {}).get("LongTermDebtCoverage", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["LongTermDebtCoverage"] = "N/A"
                return evaluated_metrics
            
            if not long_debt_cov:
                evaluated_metrics["LongTermDebtCoverage"] = "N/A"
            else:
                if long_debt_cov <= 0:
                    evaluated_metrics["LongTermDebtCoverage"] = "Not Good (In Debt)"
                else:
                    evaluated_metrics["LongTermDebtCoverage"] = "Good"

            # Assets Growth
        if "TotalAssetsCAGR" in metrics.get('liquidity', {}):
            try:
                total_assets_cagr = round(float(metrics.get('liquidity', {}).get("TotalAssetsCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["TotalAssetsCAGR"] = "N/A"
                return evaluated_metrics
            
            if not total_assets_cagr:
                evaluated_metrics["TotalAssetsCAGR"] = "N/A"
            else:
                if total_assets_cagr <= 0:
                    evaluated_metrics["TotalAssetsCAGR"] = "Not Good"
                else:
                    evaluated_metrics["TotalAssetsCAGR"] = "Good"

            # Liabilities Growth
        if "TotalLiabilitiesCAGR" in metrics.get('liquidity', {}):
            try:
                total_liabilities_cagr = round(float(metrics.get('liquidity', {}).get("TotalLiabilitiesCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["TotalLiabilitiesCAGR"] = "N/A"
                return evaluated_metrics
            
            if not total_liabilities_cagr:
                evaluated_metrics["TotalLiabilitiesCAGR"] = "N/A"
            else:
                if total_liabilities_cagr <= 0:
                    evaluated_metrics["TotalLiabilitiesCAGR"] = "Good"
                else:
                    evaluated_metrics["TotalLiabilitiesCAGR"] = "Not Good"

            # Stockholders Equity
        if "StockholdersEquityCAGR" in metrics.get('liquidity', {}):
            try:
                stockholders_equity_cagr = round(float(metrics.get('liquidity', {}).get("StockholdersEquityCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["StockholdersEquityCAGR"] = "N/A"
                return evaluated_metrics
            
            if not stockholders_equity_cagr:
                evaluated_metrics["StockholdersEquityCAGR"] = "N/A"
            else:
                if stockholders_equity_cagr <= 0:
                    evaluated_metrics["StockholdersEquityCAGR"] = "Not Good"
                else:
                    evaluated_metrics["StockholdersEquityCAGR"] = "Good"

        # Cash
            # Free Cashflow Yield
        if "FreeCashflowYield" in metrics.get('cashflow', {}):
            try:
                free_cashflow_yield = round(float(metrics.get('cashflow', {}).get("FreeCashflowYield", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["FreeCashflowYield"] = "N/A"
                return evaluated_metrics
            
            if not free_cashflow_yield:
                evaluated_metrics["FreeCashflowYield"] = "N/A"
            else:
                if free_cashflow_yield <= 2:
                    evaluated_metrics["FreeCashflowYield"] = "Overvalued / Bad to Generate Cash"
                elif free_cashflow_yield <=5:
                    evaluated_metrics["FreeCashflowYield"] = "Healthy / Consistent to Generates Cash"
                else:
                    evaluated_metrics["FreeCashflowYield"] = "Undervalued / Highly Profitable"

        # Ratios
            # Current Ratio
        if "CurrentRatio" in metrics.get('ratios', {}):
            try:
                current_ratio = round(float(metrics.get('ratios', {}).get("CurrentRatio", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["CurrentRatio"] = "N/A"
                return evaluated_metrics
            
            if not current_ratio:
                evaluated_metrics["CurrentRatio"] = "N/A"
            else:
                if current_ratio <= 100:
                    evaluated_metrics["CurrentRatio"] = "Not Good (In Debt)"
                elif current_ratio <=120:
                    evaluated_metrics["CurrentRatio"] = "Tight Margin to Debt"
                elif current_ratio <=200:
                    evaluated_metrics["CurrentRatio"] = "Good Debt Coverage"
                else:
                    evaluated_metrics["CurrentRatio"] = "Perfect Coverage (Duoble +)"

            # Current Ratio Growth
        if "CurrentRatioCAGR" in metrics.get('ratios', {}):
            try:
                current_ratio_cagr = round(float(metrics.get('ratios', {}).get("CurrentRatioCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["CurrentRatioCAGR"] = "N/A"
                return evaluated_metrics
            
            if not current_ratio_cagr:
                evaluated_metrics["CurrentRatioCAGR"] = "N/A"
            else:
                if current_ratio_cagr <= 0:
                    evaluated_metrics["CurrentRatioCAGR"] = "Not Good"
                else:
                    evaluated_metrics["CurrentRatioCAGR"] = "Good"

            # Cash Ratio
        if "CashRatio" in metrics.get('ratios', {}):
            try:
                cash_ratio = round(float(metrics.get('ratios', {}).get("CashRatio", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["CashRatio"] = "N/A"
                return evaluated_metrics
            
            if not cash_ratio:
                evaluated_metrics["CashRatio"] = "N/A"
            else:
                if cash_ratio <= 50:
                    evaluated_metrics["CashRatio"] = "Not Good (In Debt)"
                elif cash_ratio <=100:
                    evaluated_metrics["CashRatio"] = "Good Debt Coverage"
                else:
                    evaluated_metrics["CashRatio"] = "Good Debt Coverage(Too Conservative)"

            # Current Ratio Growth
        if "CashRatioCAGR" in metrics.get('ratios', {}):
            try:
                cash_ratio_cagr = round(float(metrics.get('ratios', {}).get("CashRatioCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["CashRatioCAGR"] = "N/A"
                return evaluated_metrics
            
            if not cash_ratio_cagr:
                evaluated_metrics["CashRatioCAGR"] = "N/A"
            else:
                if cash_ratio_cagr <= 0:
                    evaluated_metrics["CashRatioCAGR"] = "Not Good"
                else:
                    evaluated_metrics["CashRatioCAGR"] = "Good"

            # Gross Margin
        if "GrossMargin" in metrics.get('ratios', {}):
            try:
                gross_margin = round(float(metrics.get('ratios', {}).get("GrossMargin", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["GrossMargin"] = "N/A"
                return evaluated_metrics
            
            if not gross_margin:
                evaluated_metrics["GrossMargin"] = "N/A"
            else:
                if gross_margin <= 25:
                    evaluated_metrics["GrossMargin"] = "Not Good - Short Margins or High Costs"
                elif gross_margin <= 40:
                    evaluated_metrics["GrossMargin"] = "Healthy - Healthy Margins Good Management"
                else:
                    evaluated_metrics["GrossMargin"] = "Good - Eficient Costs Management"

            # Gross Margin Growth
        if "GrossMarginCAGR" in metrics.get('ratios', {}):
            try:
                gross_margin_cagr = round(float(metrics.get('ratios', {}).get("GrossMarginCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["GrossMarginCAGR"] = "N/A"
                return evaluated_metrics
            
            if not gross_margin_cagr:
                evaluated_metrics["GrossMarginCAGR"] = "N/A"
            else:
                if gross_margin_cagr <= 0:
                    evaluated_metrics["GrossMarginCAGR"] = "Not Good"
                else:
                    evaluated_metrics["GrossMarginCAGR"] = "Good"

            # Operating Margin
        if "OperatingMargin" in metrics.get('ratios', {}):
            try:
                operating_margin = round(float(metrics.get('ratios', {}).get("OperatingMargin", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["OperatingMargin"] = "N/A"
                return evaluated_metrics
            
            if not operating_margin:
                evaluated_metrics["OperatingMargin"] = "N/A"
            else:
                if operating_margin <= 10:
                    evaluated_metrics["OperatingMargin"] = "Not Good - High Operational Costs or Dificulties to Get Revenue"
                elif operating_margin <= 20:
                    evaluated_metrics["OperatingMargin"] = "Healthy - Healthy Operational Management"
                else:
                    evaluated_metrics["OperatingMargin"] = "Good - Eficient Costs Management"

            # Operational Margin Growth
        if "OperatingMarginCAGR" in metrics.get('ratios', {}):
            try:
                operating_margin_cagr = round(float(metrics.get('ratios', {}).get("OperatingMarginCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["OperatingMarginCAGR"] = "N/A"
                return evaluated_metrics
            
            if not operating_margin_cagr:
                evaluated_metrics["OperatingMarginCAGR"] = "N/A"
            else:
                if operating_margin_cagr <= 0:
                    evaluated_metrics["OperatingMarginCAGR"] = "Not Good"
                else:
                    evaluated_metrics["OperatingMarginCAGR"] = "Good"
            
            # Profit Margin
        if "ProfitMargin" in metrics.get('ratios', {}):
            try:
                profit_margin = round(float(metrics.get('ratios', {}).get("ProfitMargin", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["ProfitMargin"] = "N/A"
                return evaluated_metrics
            
            if not profit_margin:
                evaluated_metrics["ProfitMargin"] = "N/A"
            else:
                if profit_margin <= 5:
                    evaluated_metrics["ProfitMargin"] = "Not Good - High Operational Costs or Operational Problems"
                elif profit_margin <= 10:
                    evaluated_metrics["ProfitMargin"] = "Moderated - Potential but Need Improvements"
                elif profit_margin <= 20:
                    evaluated_metrics["ProfitMargin"] = "Healthy - Healthy and Solid Management"
                else:
                    evaluated_metrics["ProfitMargin"] = "Good - Highly Profitable and Eficient Profit Generate"

            # Profit Margin Growth
        if "ProfitMarginCAGR" in metrics.get('ratios', {}):
            try:
                profit_margin_cagr = round(float(metrics.get('ratios', {}).get("ProfitMarginCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["ProfitMarginCAGR"] = "N/A"
                return evaluated_metrics
            
            if not profit_margin_cagr:
                evaluated_metrics["ProfitMarginCAGR"] = "N/A"
            else:
                if profit_margin_cagr <= 0:
                    evaluated_metrics["ProfitMarginCAGR"] = "Not Good"
                else:
                    evaluated_metrics["ProfitMarginCAGR"] = "Good"
            
            # Return On Equity
        if "ReturnOnEquity" in metrics.get('ratios', {}):
            try:
                return_on_equity = round(float(metrics.get('ratios', {}).get("ReturnOnEquity", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["ReturnOnEquity"] = "N/A"
                return evaluated_metrics
            
            if not return_on_equity:
                evaluated_metrics["ReturnOnEquity"] = "N/A"
            else:
                if return_on_equity <= 10:
                    evaluated_metrics["ReturnOnEquity"] = "Not Good - Low Eficiency on Equity Use"
                elif return_on_equity <= 15:
                    evaluated_metrics["ReturnOnEquity"] = "Moderated - Potential but Need Improvements"
                elif return_on_equity <= 20:
                    evaluated_metrics["ReturnOnEquity"] = "Healthy - Healthy and Eficient Management"
                else:
                    evaluated_metrics["ReturnOnEquity"] = "Good - Highly Eficient Profit Generate"

            # Return On Equity Growth
        if "ReturnOnEquityCAGR" in metrics.get('ratios', {}):
            try:
                return_on_equity_cagr = round(float(metrics.get('ratios', {}).get("ReturnOnEquityCAGR", "N/A")), 2)
            except (ValueError, TypeError):
                evaluated_metrics["ReturnOnEquityCAGR"] = "N/A"
                return evaluated_metrics
            
            if not return_on_equity_cagr:
                evaluated_metrics["ReturnOnEquityCAGR"] = "N/A"
            else:
                if return_on_equity_cagr <= 0:
                    evaluated_metrics["ReturnOnEquityCAGR"] = "Not Good"
                else:
                    evaluated_metrics["ReturnOnEquityCAGR"] = "Good"
            
        

        return evaluated_metrics if evaluated_metrics else "Indefinido"
 

