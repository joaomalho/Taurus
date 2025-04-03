import talib
import pandas as pd
from backend.risk_manager.risk_manager import RiskManagerTechnical

class TrendMetrics():
    """
    A class that encapsulates technical analysis metrics using TA-Lib.
    """

    def __init__(self):
        self

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

        rmt = RiskManagerTechnical()
        crossover_signal = rmt.signal_decision_crossover(ema_low, ema_mid, ema_high)

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

        rmt = RiskManagerTechnical()
        adx_signal = rmt.signal_decision_adx(adx_now)

        return {
            "symbol": symbol,
            "length": length,
            "adx_now": round(adx_now, 4),
            "signal": adx_signal
        }

    ### Volatility ###
    def get_bollinger_bands(self, symbol, close_prices, length, std_dev):
        """
        This function calculates Bollinger Bands and detects signals based on them.
        
        Parameters:
        - data: DataFrame containing the price data with a 'close' column.
        - length: SMA period.
        - std_dev: Number of standard deviations for the bands.
        
        Returns:
        - Updates self.bbands_signal with 'Buy', 'Sell', or 'Flat'.
        """

        if close_prices.size < length:
            return {"error": "Dados insuficientes para calcular ADX"}
        
        upper_band, middle_band, lower_band = talib.BBANDS(
            close_prices, timeperiod=length, nbdevup=std_dev, nbdevdn=std_dev, matype=0
        )

        last_close = close_prices[-1]
        lower_band, middle_band, upper_band = lower_band[-1], middle_band[-1], upper_band[-1]
        
        rmt = RiskManagerTechnical()
        bbands_signal = rmt.signal_decision_bbands(last_close, lower_band, upper_band)
        return {
            "symbol": symbol,
            "length": length,
            "std_dev": std_dev,
            "upper_band": upper_band,
            "middle_band": middle_band,
            "lower_band": lower_band,
            "signal": bbands_signal
        }

    ### Oscilators ###
    def get_rsi(self, symbol, close_prices, length, overbought, oversold):
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

        length, upper_level, lower_level = length, overbought, oversold 

        rsi = talib.RSI(close_prices, timeperiod=length)
        rsi_now = rsi[-1]

        rmt = RiskManagerTechnical()
        rsi_signal = rmt.signal_decision_rsi(rsi_now, upper_level, lower_level)

        return {
            "symbol": symbol,
            "length": length,
            "rsi": rsi_now,
            "upper_level": upper_level,
            "lower_level": lower_level,
            "signal": rsi_signal
        }