import talib
import pandas as pd

class TrendMetrics():
    """
    A class that encapsulates technical analysis metrics using TA-Lib.
    """

    def __init__(self, data):
        self.data = data
        self.result_df = pd.DataFrame(columns=['function', 'signal'])
        self.crossover_info = pd.DataFrame(columns=['function', 'signal', 'period_low', 'period_mid', 'period_high', 'ema_low', 'ema_mid', 'ema_high'])
        self.sma_bands_info = pd.DataFrame(columns=['function', 'signal', 'period', 'std', 'lower_band', 'middle_band', 'upper_band'])
        self.rsi_info = pd.DataFrame(columns=['function', 'signal', 'period', 'upper_level', 'lower_level'])

    def get_crossover(self, data: pd.DataFrame, l1: int, l2: int, l3: int):
        """
        This function measures the crossover of 3 EMAs using TA-Lib.
        
        Parameters:
        - data: DataFrame containing the price data with a 'close' column.
        - l1, l2, l3: Periods for the 3 EMAs.
        
        Returns:
        - Updates self.crossover_signal with 'Buy', 'Sell', or 'Flat'.
        """
        period_low, period_mid, period_high = l1, l2, l3
        
        # Compute EMAs
        ema1 = talib.EMA(data['close'], timeperiod=l1)
        ema2 = talib.EMA(data['close'], timeperiod=l2)
        ema3 = talib.EMA(data['close'], timeperiod=l3)

        # Current values
        ema_low, ema_mid, ema_high = ema1.iloc[-1], ema2.iloc[-1], ema3.iloc[-1]

        # Determine signal
        if ema_low > ema_mid > ema_high:
            crossover_signal = 'Buy'
        elif ema_low < ema_mid < ema_high:
            crossover_signal = 'Sell'
        else:
            crossover_signal = 'Flat'

        # Save result
        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'function': ['Crossover'],
            'signal': [crossover_signal]
        })], ignore_index=True)

        # Save result
        self.crossover_info = pd.concat([self.crossover_info, pd.DataFrame({
            'function': ['Crossover'],
            'signal': [crossover_signal],
            'period_low': [period_low],
            'period_mid': [period_mid],
            'period_high': [period_high],
            'ema1_now': [ema_low],
            'ema2_now': [ema_mid],
            'ema3_now': [ema_high],
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

        period, std = length, std_dev

        # Compute Bollinger Bands
        upper_band, middle_band, lower_band = talib.BBANDS(
            data['close'], timeperiod=length, nbdevup=std_dev, nbdevdn=std_dev, matype=0
        )

        # Current values
        last_close = data['close'].iloc[-1]
        lower_band, middle_band, upper_band = lower_band.iloc[-1], middle_band.iloc[-1], upper_band.iloc[-1]

        # Determine signal
        if last_close <= lower_band:
            bbands_signal = 'Buy'
        elif last_close >= upper_band:
            bbands_signal = 'Sell'
        else:
            bbands_signal = 'Flat'

        # Save result
        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'function': ['Bollinger_Bands'],
            'signal': [bbands_signal]
        })], ignore_index=True)
        
        self.sma_bands_info = pd.concat([self.sma_bands_info, pd.DataFrame({
            'function': ['Bollinger_Bands'],
            'signal': [bbands_signal],
            'period': [period],
            'std': [std],
            'lower_band': [lower_band],
            'middle_band': [middle_band],
            'upper_band': [upper_band]
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

        period, upper_level, lower_level = length, overbought, oversold 

        # Compute RSI
        rsi = talib.RSI(data['close'], timeperiod=length)
        rsi_now = rsi.iloc[-1]

        # Determine signal
        if rsi_now >= overbought:
            rsi_signal = 'Sell'
        elif rsi_now <= oversold:
            rsi_signal = 'Buy'
        else:
            rsi_signal = 'Flat'

        # Save result
        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'function': ['RSI'],
            'signal': [rsi_signal]
        })], ignore_index=True)

        self.rsi_info = pd.concat([self.sma_bands_info, pd.DataFrame({
            'function': ['Bollinger_Bands'],
            'signal': [rsi_signal],
            'period': [period],
            'upper_level': [upper_level],
            'lower_level': [lower_level]
        })], ignore_index=True)
