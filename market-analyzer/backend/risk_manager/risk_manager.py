'''
Collect data from candles
 - Detection + Relevance + Signal + Stop-loss

Collect data from trend Metrics
 - Detection + Relevance + Signal + Stop-loss
'''


class RiskManager():

    def __init__(self):
        self.stoploss = None
        self.takeprofit = None

    def get_majority(self):
        '''
        This function get the majority of signal
        '''
        pass

    def relevance_candle(self):
        '''
        Determine whether the targets have already been reached following pattern detection, if not, consider them as active targets. 
        Additionally, evaluate which pattern should be prioritized if multiple patterns are detected.
        '''

    def stoploss_manager():
        pass

    def take_profit_manager():
        pass

    def decision_manager():
        '''
        Trend confirmation:
            1. Crossoover signal Buy or Sell 
            2. ADX > Threshold (storng trend)
            3. MACD line cross signal Line to MACD < Signal line then Buy, MACD > Signal Line then Sell        
        '''
        pass
    
    def evaluate_metrics(self, metrics):
        """
        Evaluate fundamental metrics.
        """

        evaluated_metrics = {}

        # Valuation
        if "trailingPE" in metrics.get('valuation', {}) and "sectorTrailingPE" in metrics.get('valuation', {}) and "forwardPE" in metrics.get('valuation', {}):
            try:
                trailing_pe = metrics.get('valuation', {}).get("trailingPE", "N/A")
                sector_pe = metrics.get('valuation', {}).get("sectorTrailingPE", "N/A")
                forward_pe = metrics.get('valuation', {}).get("forwardPE", "N/A")
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
                peg_ratio = metrics.get('valuation', {}).get("PEGRatio", "N/A")
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
                div_coverage_ratio = metrics.get('dividends', {}).get("divCoverageRate", "N/A")
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
                cost_revenue_cagr = metrics.get('profitability', {}).get("CostOfRevenueCAGR", "N/A")
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
                total_revenue_cagr = metrics.get('profitability', {}).get("TotalRevenueCAGR", "N/A")
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
                net_worth = metrics.get('liquidity', {}).get("NetWorth", "N/A")
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
                short_debt_cov = metrics.get('liquidity', {}).get("ShortTermDebtCoverage", "N/A")
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
                long_debt_cov = metrics.get('liquidity', {}).get("LongTermDebtCoverage", "N/A")
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
                total_assets_cagr = metrics.get('liquidity', {}).get("TotalAssetsCAGR", "N/A")
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
                total_liabilities_cagr = metrics.get('liquidity', {}).get("TotalLiabilitiesCAGR", "N/A")
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
                stockholders_equity_cagr = metrics.get('liquidity', {}).get("StockholdersEquityCAGR", "N/A")
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
                free_cashflow_yield = metrics.get('cashflow', {}).get("FreeCashflowYield", "N/A")
            except (ValueError, TypeError):
                evaluated_metrics["FreeCashflowYield"] = "N/A"
                return evaluated_metrics
            
            if not free_cashflow_yield:
                evaluated_metrics["FreeCashflowYield"] = "N/A"
            else:
                if free_cashflow_yield <= 2:
                    evaluated_metrics["FreeCashflowYield"] = "Overvalued / Bad to Generate Cash."
                elif free_cashflow_yield <=5:
                    evaluated_metrics["FreeCashflowYield"] = "Healthy / Consistent to Generates Cash"
                else:
                    evaluated_metrics["FreeCashflowYield"] = "Undervalued / Highly Profitable"


        return evaluated_metrics if evaluated_metrics else "Indefinido"

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
    

        
        

