
import talib
import numpy as np
import pandas as pd

class CandlestickData():
    """
    A class that passes information for chat metrics draw
    """

    def __init__(self):
        self

    def get_ema_history(self, data, fastperiod: int, mediumperiod: int, slowperiod: int):
        """
        Retorna os valores históricos das 3 EMAs (fast, medium, slow).
        """

        close_prices = data.Close
        dates = data.Date

        if close_prices.size < slowperiod:
            return {"error": "Dados insuficientes para calcular EMAs"}

        ema1 = talib.EMA(close_prices, timeperiod=fastperiod)
        ema2 = talib.EMA(close_prices, timeperiod=mediumperiod)
        ema3 = talib.EMA(close_prices, timeperiod=slowperiod)

        # Converter strings para datetime
        dates = pd.to_datetime(dates)

        ema_fast = [
            {"time": str(dates[i].date()), "value": float(ema1[i])}
            for i in range(len(ema1)) if not np.isnan(ema1[i])
        ]
        ema_medium = [
            {"time": str(dates[i].date()), "value": float(ema2[i])}
            for i in range(len(ema2)) if not np.isnan(ema2[i])
        ]
        ema_slow = [
            {"time": str(dates[i].date()), "value": float(ema3[i])}
            for i in range(len(ema3)) if not np.isnan(ema3[i])
        ]

        return {
            "symbol": data.get("Symbol", "N/A") if isinstance(data, dict) else "N/A",
            "ema_fast": ema_fast,
            "ema_medium": ema_medium,
            "ema_slow": ema_slow
        }
    

    ### Volatility ###
    def get_bollinger_bands_history(self, data, length : int, std_dev :int):
        """
        This function calculates Bollinger Bands and detects signals based on them.
        
        Parameters:
        - data: DataFrame containing the price data with a 'close' column.
        - length: SMA period.
        - std_dev: Number of standard deviations for the bands.
        
        Returns:
        - Updates self.bbands_signal with 'Buy', 'Sell', or 'Flat'.
        """

        close_prices = data.Close
        dates = pd.to_datetime(data.Date)

        if close_prices.size < length:
            return {"error": "Dados insuficientes para calcular Bollinger Bands"}

        upper, middle, lower = talib.BBANDS(
            close_prices, timeperiod=length, nbdevup=std_dev, nbdevdn=std_dev, matype=0
        )

        bb_upper = [
            {"time": str(dates[i].date()), "value": float(upper[i])}
            for i in range(len(upper)) if not np.isnan(upper[i])
        ]
        bb_middle = [
            {"time": str(dates[i].date()), "value": float(middle[i])}
            for i in range(len(middle)) if not np.isnan(middle[i])
        ]
        bb_lower = [
            {"time": str(dates[i].date()), "value": float(lower[i])}
            for i in range(len(lower)) if not np.isnan(lower[i])
        ]

        return {
            "symbol": data.get("Symbol", "N/A") if isinstance(data, dict) else "N/A",
            "bb_upper": bb_upper,
            "bb_middle": bb_middle,
            "bb_lower": bb_lower
        }