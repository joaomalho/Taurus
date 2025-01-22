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
    
