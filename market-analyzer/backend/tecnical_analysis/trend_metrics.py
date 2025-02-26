import talib
import pandas as pd
import numpy as np

class TrendMetrics():
    """
    A class that encapsulates technical analysis metrics using TA-Lib.
    """

    def __init__(self):
        self.sma_bands_info = pd.DataFrame(columns=['function', 'signal', 'period', 'std', 'lower_band', 'middle_band', 'upper_band'])
        self.rsi_info = pd.DataFrame(columns=['function', 'signal', 'period', 'upper_level', 'lower_level'])
        self.macd_info = pd.DataFrame(columns=['function', 'signal', 'period', 'upper_level', 'lower_level'])

    ### Trend Metrics ###
    def get_crossover(self, close_prices, symbol, fastperiod: int, mediumperiod: int, slowperiod: int):
        """
        This function measures the crossover of 3 EMAs using TA-Lib.
        
        Parameters:
        - data: DataFrame containing the price data with a 'close' column.
        - l1, l2, l3: Periods for the 3 EMAs.
        
        Returns:
        - Updates self.crossover_signal with 'Buy', 'Sell', or 'Flat'.
        """
        if close_prices.size < slowperiod:
            return {"error": "Dados insuficientes para calcular EMAs"}

        ema1 = talib.EMA(close_prices, timeperiod=fastperiod)
        ema2 = talib.EMA(close_prices, timeperiod=mediumperiod)
        ema3 = talib.EMA(close_prices, timeperiod=slowperiod)

        ema_low, ema_mid, ema_high = ema1[-1], ema2[-1], ema3[-1]

        if ema_low > ema_mid > ema_high:
            crossover_signal = 'Buy'
        elif ema_low < ema_mid < ema_high:
            crossover_signal = 'Sell'
        else:
            crossover_signal = 'Flat'

        return {
            "symbol": symbol,
            "fast_period": fastperiod,
            "medium_period": mediumperiod,
            "slow_period": slowperiod,
            "ema1_now": round(ema_low, 4),
            "ema2_now": round(ema_mid, 4),
            "ema3_now": round(ema_high, 4),
            "signal": crossover_signal
        }

    def get_adx(self, high_prices, low_prices, close_prices, symbol, length: int):
        """
        This function calculates the ADX (Average Directional Index) to measure trend strength.

        Parameters:
        - high_prices: np.array containing the high prices.
        - low_prices: np.array containing the low prices.
        - close_prices: np.array containing the close prices.
        - symbol: Stock symbol (string).
        - length: Period for ADX calculation.

        Returns:
        - Dictionary with ADX value and trend strength signal.
        """
        
        if close_prices.size < length:
            return {"error": "Dados insuficientes para calcular ADX"}

        adx = talib.ADX(high_prices, low_prices, close_prices, timeperiod=length)
        
        adx_now = adx[-1]

        adx_signal = 'Strong Trend' if adx_now > 25 else 'Weak Trend'

        return {
            "symbol": symbol,
            "length": length,
            "adx_now": round(adx_now, 4),
            "signal": adx_signal
        }


    def get_macd(self, data: pd.DataFrame, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        """
        This function calculates the MACD (Moving Average Convergence Divergence).
        
        Parameters:
        - data: DataFrame containing the 'Close' column.
        - fastperiod: Short-term EMA period.
        - slowperiod: Long-term EMA period.
        - signalperiod: Signal line EMA period.
        
        Returns:
        - Updates self.result_df with MACD signals.
        """

        macd, macd_signal, macd_hist = talib.MACD(
            data['Close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod
        )
        macd_now, macd_signal_now = macd.iloc[-1], macd_signal.iloc[-1]
        macd_signal_value = 'Buy' if macd_now > macd_signal_now else 'Sell' if macd_now < macd_signal_now else 'Flat'
        
        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'function': ['MACD'],
            'signal': [macd_signal_value]
        })], ignore_index=True)

        self.macd_info = pd.concat([self.macd_info, pd.DataFrame({
            'function': ['ADX'],
            'signal': [macd_signal],
            'fast_period': [fastperiod],
            'low_period': [slowperiod],
            'signal_period': [signalperiod]
        })], ignore_index=True)

    ### Volatility ###
    def get_sma_bands(self, data: pd.DataFrame, length: int=15, std_dev: int = 1):
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

        upper_band, middle_band, lower_band = talib.BBANDS(
            data['Close'], timeperiod=length, nbdevup=std_dev, nbdevdn=std_dev, matype=0
        )

        last_close = data['Close'].iloc[-1]
        lower_band, middle_band, upper_band = lower_band.iloc[-1], middle_band.iloc[-1], upper_band.iloc[-1]

        if last_close <= lower_band:
            bbands_signal = 'Buy'
        elif last_close >= upper_band:
            bbands_signal = 'Sell'
        else:
            bbands_signal = 'Flat'

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

    ### Oscilators ###
    def get_rsi(self, data: pd.DataFrame, length: int = 25, overbought: int = 70, oversold: int = 30):
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

        rsi = talib.RSI(data['Close'], timeperiod=length)
        rsi_now = rsi.iloc[-1]

        if rsi_now >= overbought:
            rsi_signal = 'Sell'
        elif rsi_now <= oversold:
            rsi_signal = 'Buy'
        else:
            rsi_signal = 'Flat'

        self.result_df = pd.concat([self.result_df, pd.DataFrame({
            'function': ['RSI'],
            'signal': [rsi_signal]
        })], ignore_index=True)

        self.rsi_info = pd.concat([self.rsi_info, pd.DataFrame({
            'function': ['RSI'],
            'signal': [rsi_signal],
            'period': [period],
            'upper_level': [upper_level],
            'lower_level': [lower_level]
        })], ignore_index=True)

