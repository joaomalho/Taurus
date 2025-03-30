
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
            "symbol": "AAPL",
            "ema_fast": ema_fast,
            "ema_medium": ema_medium,
            "ema_slow": ema_slow
        }