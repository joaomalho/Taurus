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

        if 'QuickRatio' in metrics.get('liquidity_and_solvency', {}):
            quick_ratio = metrics.get('liquidity_and_solvency', {}).get('QuickRatio', 'N/A')
            if quick_ratio == "N/A":
                evaluated_metrics["QuickRatio"] = "N/A"
            elif quick_ratio < 0.75:
                evaluated_metrics["QuickRatio"] = "Very Negative"
            elif quick_ratio < 1:
                evaluated_metrics["QuickRatio"] = "Negative"
            elif quick_ratio < 1.5:
                evaluated_metrics["QuickRatio"] = "Neutral"
            elif quick_ratio < 2:
                evaluated_metrics["QuickRatio"] = "Positive"
            else:
                evaluated_metrics["QuickRatio"] = "Very Positive"

        if 'CurrentRatio' in metrics.get('liquidity_and_solvency', {}):
            current_ratio = metrics.get('liquidity_and_solvency', {}).get('CurrentRatio', 'N/A')
            if current_ratio == "N/A":
                evaluated_metrics["CurrentRatio"] = "N/A"
            elif current_ratio < 0.75:
                evaluated_metrics["CurrentRatio"] = "Very Negative"
            elif current_ratio < 1:
                evaluated_metrics["CurrentRatio"] = "Negative"
            elif current_ratio < 1.5:
                evaluated_metrics["CurrentRatio"] = "Neutral"
            elif current_ratio < 2:
                evaluated_metrics["CurrentRatio"] = "Positive"
            else:
                evaluated_metrics["CurrentRatio"] = "Very Positive"

        if 'CashRatio' in metrics.get('liquidity_and_solvency', {}):
            cash_ratio = metrics.get('liquidity_and_solvency', {}).get('CashRatio', 'N/A')
            if cash_ratio == "N/A":
                evaluated_metrics["CashRatio"] = "N/A"
            elif cash_ratio < 0.75:
                evaluated_metrics["CashRatio"] = "Very Negative"
            elif cash_ratio < 1:
                evaluated_metrics["CashRatio"] = "Negative"
            elif cash_ratio < 1.5:
                evaluated_metrics["CashRatio"] = "Neutral"
            elif cash_ratio < 2:
                evaluated_metrics["CashRatio"] = "Positive"
            else:
                evaluated_metrics["CashRatio"] = "Very Positive"

        if 'DebttoEquity' in metrics.get('liquidity_and_solvency', {}):
            debt_to_equity = metrics.get('liquidity_and_solvency', {}).get('DebttoEquity', 'N/A')
            if debt_to_equity == "N/A":
                evaluated_metrics["DebttoEquity"] = "N/A"
            elif debt_to_equity > 2.5:
                evaluated_metrics["DebttoEquity"] = "Very Negative"
            elif debt_to_equity > 1.8:
                evaluated_metrics["DebttoEquity"] = "Negative"
            elif debt_to_equity > 1.2:
                evaluated_metrics["DebttoEquity"] = "Neutral"
            elif debt_to_equity > 0.7:
                evaluated_metrics["DebttoEquity"] = "Positive"
            else:
                evaluated_metrics["DebttoEquity"] = "Very Positive"

        if 'DebttoAssetsRatio' in metrics.get('liquidity_and_solvency', {}):
            debt_to_assets = metrics.get('liquidity_and_solvency', {}).get('DebttoAssetsRatio', 'N/A')
            if debt_to_assets == "N/A":
                evaluated_metrics["DebttoAssetsRatio"] = "N/A"
            elif debt_to_assets > 2.5:
                evaluated_metrics["DebttoAssetsRatio"] = "Very Negative"
            elif debt_to_assets > 1.8:
                evaluated_metrics["DebttoAssetsRatio"] = "Negative"
            elif debt_to_assets > 1.2:
                evaluated_metrics["DebttoAssetsRatio"] = "Neutral"
            elif debt_to_assets > 0.7:
                evaluated_metrics["DebttoAssetsRatio"] = "Positive"
            else:
                evaluated_metrics["DebttoAssetsRatio"] = "Very Positive"

        if 'InterestCoverageRatio' in metrics.get('liquidity_and_solvency', {}):
            interest_cover_ratio = metrics.get('liquidity_and_solvency', {}).get('InterestCoverageRatio', 'N/A')
            if interest_cover_ratio == "N/A":
                evaluated_metrics["InterestCoverageRatio"] = "N/A"
            elif interest_cover_ratio < 1:
                evaluated_metrics["InterestCoverageRatio"] = "Very Negative"
            elif interest_cover_ratio < 2:
                evaluated_metrics["InterestCoverageRatio"] = "Negative"
            elif interest_cover_ratio < 3:
                evaluated_metrics["InterestCoverageRatio"] = "Neutral"
            elif interest_cover_ratio < 5:
                evaluated_metrics["InterestCoverageRatio"] = "Positive"
            else:
                evaluated_metrics["InterestCoverageRatio"] = "Very Positive"

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

        if "divCoverageRate" in metrics.get('dividends_and_buybacks', {}):
            try:
                div_coverage_ratio = metrics.get('dividends_and_buybacks', {}).get("divCoverageRate", "N/A")
            except (ValueError, TypeError):
                evaluated_metrics["divCoverageRate"] = "N/A"
                return evaluated_metrics
            
            if not div_coverage_ratio:
                evaluated_metrics["divCoverageRate"] = "N/A"
            else:
                if div_coverage_ratio <= 1:
                    evaluated_metrics["divCoverageRate"] = "No Coverage"
                elif div_coverage_ratio <= 1.5:
                    evaluated_metrics["divCoverageRate"] = "Bad Coverage"
                elif div_coverage_ratio <= 3:
                    evaluated_metrics["divCoverageRate"] = "Good Coverage"
                else:
                    evaluated_metrics["divCoverageRate"] = "Greedy Coverage"
    

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
    

        
        

