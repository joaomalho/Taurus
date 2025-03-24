'''
This file measures the fibonacci retracement levels, and where price is in relation of it.
'''

import pandas as pd

class Fibonacci_Retracement():
    def __init__(self) -> None:
        
        self.result_df = pd.DataFrame(columns=['Function', 'Signal', 'Relevance'])
        
        self.fibo_relevance = None
        self.Fib0 = None
        self.Fib100 = None 
        self.fibo_order = None
        self.fibo_signal = None
    
    # Fibonacci Retracement Levels
    def fibonacci_retracement_levels(self, daily_data, current_price):
        '''
        This function measure the fibonacci retracement levels in a timeline of 1daily which is the minimum applicable
        
        Fundamentals:
        
            * Fibonacci retracement levels—stemming from the Fibonacci sequence—are horizontal lines that indicate where support 
            and resistance are likely to occur.
            * Each level is associated with a percentage. The percentage is how much of a prior move the price has retraced. 
            * The Fibonacci retracement levels are 23.6%, 38.2%, 61.8%, and 78.6%. While not officially a Fibonacci ratio, 50% is also used.

        Conditions:
            
            * Relevance is the weight of the distance, if 80 % in a Descendent trend the price tendenci of turn to a bulish is ~80%
            * Timeline = 1 daily candles
            * Higher Extreme = High value (Shadow)
            * Lower Extreme = Low value (Shadow)
            
            * Bullish - Diff = max_level - min_level
                        Fib100 = min_level
                        Fib764 = max_index - (Diff * 0.764)
                        Fib618 = max_index - (Diff * 0.618)
                        Fib50 = max_index - (Diff * 0.5)
                        Fib382 = max_index - (Diff * 0.382)
                        Fib236 = max_index - (Diff * 0.236)
                        Fib0 = max_index

            * Bearish - Diff = max_level - min_level
                        Fib100 = max_level
                        Fib764 = min_level + (Diff * 0.764)
                        Fib618 = min_level + (Diff * 0.618)
                        Fib50 = min_level + (Diff * 0.5)
                        Fib382 = min_level + (Diff * 0.382)
                        Fib236 = min_level + (Diff * 0.236)
                        Fib0 = min_level
        '''

        # Measure the simple levels
        min_level = daily_data['low'].min()
        max_level = daily_data['high'].max()

        # Get the levels Index
        min_index = daily_data['low'].idxmin()
        max_index = daily_data['high'].idxmax()

        # If necessary to check the rows of each
        # min_row = bars_sma_bb_rsi_supresis_df.iloc[min_index]
        # max_row = bars_sma_bb_rsi_supresis_df.iloc[max_index]

        # Movement is Descendent 
        if max_index < min_index:
            
            Diff = max_level - min_level
            Fib100 = (max_level)
            Fib764 = (min_level + (Diff * 0.764))
            Fib618 = (min_level + (Diff * 0.618)) 
            Fib50 = (min_level + (Diff * 0.5))
            Fib382 = (min_level + (Diff * 0.382))
            Fib236 = (min_level + (Diff * 0.236)) 
            Fib0 = (min_level) 

            # Get Relevance 

            fib_levels = [Fib100, Fib764, Fib618, Fib50, Fib382, Fib236, Fib0]

                # Calculate absolute dif between current_price and each value
            abs_dif = [abs(current_price - i) for i in fib_levels]

                # Find the index of the minimum difference
            min_index = abs_dif.index(min(abs_dif))
                
                # Get the value with the minimum difference
            fibo_relevance = fib_levels[min_index]

                #Fibo order
            fibo_order = 'Descendent'
            fibo_signal = 'Buy'
            
            self.fibo_relevance = fibo_relevance
            self.Fib0 = Fib0
            self.Fib100 = Fib100 
            self.fibo_order = fibo_order
            self.fibo_signal = fibo_signal 
        
        # Movement is Ascendent
        elif min_index < max_index:
            
            Diff = max_level - min_level
            Fib100 = (min_level) 
            Fib764 = (max_index - (Diff * 0.764)) 
            Fib618 = (max_index - (Diff * 0.618)) 
            Fib50 = (max_index - (Diff * 0.5)) 
            Fib382 = (max_index - (Diff * 0.382)) 
            Fib236 = (max_index - (Diff * 0.236)) 
            Fib0 = (max_index) 

            # Get Relevance 
                # Values
            fib_levels = [Fib100, Fib764, Fib618, Fib50, Fib382, Fib236, Fib0]

                # Calculate absolute dif between current_price and each value
            abs_dif = [abs(current_price - i) for i in fib_levels]

                # Find the index of the minimum difference
            min_index = abs_dif.index(min(abs_dif))

                # Get the value with the minimum difference
            fibo_relevance = fib_levels[min_index]
                
                #Fibo order
            fibo_order = 'Ascendent'
            fibo_signal = 'Sell'
            
            self.fibo_relevance = fibo_relevance
            self.Fib0 = Fib0
            self.Fib100 = Fib100 
            self.fibo_order = fibo_order
            self.fibo_signal = fibo_signal
                        

        # Check if 'self.result_df' is empty or all-NA
        if self.result_df is None or self.result_df.empty or self.result_df.isna().all().all():
            # Create a new DataFrame if it's empty or all-NA
            self.result_df = pd.DataFrame({
                'Function': ['Fibonacci'],
                'Signal': [self.fibo_signal],
                'Relevance': [self.fibo_relevance]
            })
        else:
            # Concatenate the new data to the existing DataFrame
            new_data = pd.DataFrame({
                'Function': ['Fibonacci'],
                'Signal': [self.fibo_signal],
                'Relevance': [self.fibo_relevance]
            })
            self.result_df = pd.concat([self.result_df, new_data], ignore_index=True)


