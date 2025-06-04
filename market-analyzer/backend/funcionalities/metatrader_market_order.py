'''
This file is responsible for market order execution
'''
import MetaTrader5 as mt5

class MarketOrderExecution():
    def __init__(self) -> None:
        
        self.order_result = None
    
    def market_order(self, tick, symbol, stoploss, take_prof, current_price, bagging_signal, volume=0.02, magic=100):
        '''
        This function will send the request to platform and request to open the position
        '''
        
        order_dict = {'Buy': 0, 'Sell': 1}
        price_dict = {'Buy': tick.ask, 'Sell': tick.bid}

        # take_profit = {'buy': upper_band - stoploss, 'sell': lower_band + stoploss}
        stop_loss = {'Buy': current_price - stoploss, 'Sell': current_price + stoploss} 
        
        request = {
            'action': mt5.TRADE_ACTION_DEAL, # action is to DEAL
            'symbol': symbol,
            'volume': volume, 
            'type': order_dict[bagging_signal], # Buy or Sell
            'price': price_dict[bagging_signal], # Buy at Curent ask price
            'magic': magic, #INT # Each order have a unique magic number to identify 
            'tp': take_prof, # Take Profit
            'sl': stop_loss[bagging_signal], # Stop Loss default
            'comment': 'python order',
            'type_time': mt5.ORDER_TIME_GTC, # Good till Cancel order
            'type_filling': mt5.ORDER_FILLING_IOC, # Imidiate or Cancel order (Used in IC markets)
        }

        order_result = mt5.order_send(request)
        
        print(order_result)
                    
        self.order_result = order_result 
            