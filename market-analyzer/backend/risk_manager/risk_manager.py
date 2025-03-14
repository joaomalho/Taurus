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

        if "QuickRatio" in metrics:
            quick_ratio = metrics.get("QuickRatio", "N/A")
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

        if "CurrentRatio" in metrics:
            current_ratio = metrics.get("CurrentRatio", "N/A")
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

        if "CashRatio" in metrics:
            cash_ratio = metrics.get("CashRatio", "N/A")
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

        if "DebttoEquity" in metrics:
            debt_to_equity = metrics.get("DebttoEquity", "N/A")
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

        if "DebttoAssetsRatio" in metrics:
            debt_to_assets = metrics.get("DebttoAssetsRatio", "N/A")
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

        if "InterestCoverageRatio" in metrics:
            interest_cover_ratio = metrics.get("InterestCoverageRatio", "N/A")
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

        if "trailingPE" in metrics and "sectorTrailingPE" in metrics and "forwardPE" in metrics:
            trailing_pe = metrics.get("trailingPE", "N/A")
            sector_pe = metrics.get("sectorTrailingPE", "N/A")
            forward_pe = metrics.get("forwardPE", "N/A")
            if trailing_pe == "N/A" and sector_pe == "N/A" and forward_pe == "N/A":
                evaluated_metrics["Pe_Valuation"] = "N/A"
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

                if score_pe == 3:
                    evaluated_metrics["Pe_Valuation"] = "Very Low Undervalued"
                elif score_pe == 2:
                    evaluated_metrics["Pe_Valuation"] = "Low Undervalued"
                elif score_pe == 1:
                    evaluated_metrics["Pe_Valuation"] = "Undervalued"
                elif score_pe == 0:
                    evaluated_metrics["Pe_Valuation"] = "Neutral Valued"
                elif score_pe == -1:
                    evaluated_metrics["Pe_Valuation"] = "Overvalued"
                elif score_pe == -2:
                    evaluated_metrics["Pe_Valuation"] = "High Overvalued"
                else:
                    evaluated_metrics["Pe_Valuation"] = "Very High Overvalued"
            
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
    

        
        

