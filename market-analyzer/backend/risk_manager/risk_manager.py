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
    
    def evaluate_metric(self, metric, value):
        """
        Evaluate a metric and return the qualitative conclusion
        """
        if value in ["N/A", None] or not isinstance(value, (int, float)):
            return "N/A"

        if metric in ["Quick Ratio", "Current Ratio", "Cash Ratio"]:
            if value < 0.75:  
                return "Very Negative"  # Muito abaixo de 1 é preocupante
            elif value < 1:  
                return "Negative"  # Ainda abaixo do ideal
            elif value < 1.5:  
                return "Neutral"  # Considerado aceitável
            elif value < 2:  
                return "Positive"  # Sinal de boa liquidez
            else:  
                return "Very Positive"  # Pode indicar excesso de liquidez

        elif metric in ["Debt to Equity (D/E)", "Debt-to-Assets Ratio"]:
            if value > 2.5:  
                return "Very Negative"  # Muito endividada
            elif value > 1.8:  
                return "Negative"  # Alto risco, mas dentro do aceitável para setores alavancados
            elif value > 1.2:  
                return "Neutral"  # Risco moderado
            elif value > 0.7:  
                return "Positive"  # Boa estrutura de capital
            else:  
                return "Very Positive"  # Empresa tem pouca dependência de dívida

        elif metric == "Interest Coverage Ratio":
            if value < 1:  
                return "Very Negative"  # Risco de insolvência
            elif value < 2:  
                return "Negative"  # Pode enfrentar dificuldades em crises
            elif value < 3:  
                return "Neutral"  # Razoável, mas precisa de monitoramento
            elif value < 5:  
                return "Positive"  # Empresa tem boa capacidade de pagar juros
            else:  
                return "Very Positive"  # Empresa tem altíssima solvência


        return "Indefinido"


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