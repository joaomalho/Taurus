import talib
import pandas as pd

class TrendMetrics:
    """
    A class that encapsulates technical analysis metrics using TA-Lib.
    """

    def __init__(self):
        self.result_df = pd.DataFrame(columns=['Function', 'Signal'])
        self.crossover_signal = None
        self.lower_band = None
        self.upper_band = None
        self.bbands_signal = None
        self.rsi_now = None
        self.rsi_signal = None

    def get_crossover(self, data: pd.DataFrame, l1: int, l2: int, l3: int):
        """
        This function measures the crossover of 3 EMAs using TA-Lib.
        
        Parameters:
        - data: DataFrame containing the price data with a 'close' column.
        - l1, l2, l3: Periods for the 3 EMAs.
        
        Returns:
        - Updates self.crossover_signal with 'Buy', 'Sell', or 'Flat'.
        """
        # Compute EMAs
        ema1 = talib.EMA(data['close'], timeperiod=l1)
        ema2 = talib.EMA(data['close'], timeperiod=l2)
        ema3 = talib.EMA(data['close'], timeperiod=l3)

        # Current values
        ema1_now, ema2_now, ema3_now = ema1.iloc[-1], ema2.iloc[-1], ema3.iloc[-1]

        # Determine signal
        if ema1_now > ema2_now > ema3_now:
            self.crossover_signal = 'Buy'
        elif ema1_now < ema2_now < ema3_now:
            self.crossover_signal = 'Sell'
        else:
            self.crossover_signal = 'Flat'

        # Save result
        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'Function': ['Crossover'],
            'Signal': [self.crossover_signal]
        })], ignore_index=True)

    def get_sma_bands(self, data: pd.DataFrame, length: int, std_dev: int):
        """
        This function calculates Bollinger Bands and detects signals based on them.
        
        Parameters:
        - data: DataFrame containing the price data with a 'close' column.
        - length: SMA period.
        - std_dev: Number of standard deviations for the bands.
        
        Returns:
        - Updates self.bbands_signal with 'Buy', 'Sell', or 'Flat'.
        """
        # Compute Bollinger Bands
        upper_band, middle_band, lower_band = talib.BBANDS(
            data['close'], timeperiod=length, nbdevup=std_dev, nbdevdn=std_dev, matype=0
        )

        # Current values
        last_close = data['close'].iloc[-1]
        self.lower_band, self.upper_band = lower_band.iloc[-1], upper_band.iloc[-1]

        # Determine signal
        if last_close <= self.lower_band:
            self.bbands_signal = 'Buy'
        elif last_close >= self.upper_band:
            self.bbands_signal = 'Sell'
        else:
            self.bbands_signal = 'Flat'

        # Save result
        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'Function': ['Bollinger_Bands'],
            'Signal': [self.bbands_signal]
        })], ignore_index=True)

    def get_rsi(self, data: pd.DataFrame, length: int, overbought: int, oversold: int):
        """
        This function calculates the RSI and generates a signal based on overbought/oversold levels.
        
        Parameters:
        - data: DataFrame containing the price data with a 'close' column.
        - length: RSI period.
        - overbought: RSI overbought threshold.
        - oversold: RSI oversold threshold.
        
        Returns:
        - Updates self.rsi_signal with 'Buy', 'Sell', or 'Flat'.
        """
        # Compute RSI
        rsi = talib.RSI(data['close'], timeperiod=length)
        self.rsi_now = rsi.iloc[-1]

        # Determine signal
        if self.rsi_now >= overbought:
            self.rsi_signal = 'Sell'
        elif self.rsi_now <= oversold:
            self.rsi_signal = 'Buy'
        else:
            self.rsi_signal = 'Flat'

        # Save result
        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'Function': ['RSI'],
            'Signal': [self.rsi_signal]
        })], ignore_index=True)
