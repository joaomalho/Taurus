import warnings
import yfinance as yf
from datetime import datetime

# Suprimir avisos específicos
warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")


class DataHistory():

    def __init__(self) -> None:
        self
    
    def get_data_history_yahoo(self, symbol : str, period : str, interval, start = '1900-01-01', end = datetime.now(), prepost : bool = True, debug : bool = True):
        '''
        Data collection from yahoo

        Parameters:
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime, inclusive. Default is 1900-01-01 E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
        end: str
            Download end date string (YYYY-MM-DD) or _datetime, exclusive. Default is now E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
        prepost : bool
            Include Pre and Post market data in results? Default is False
        debug: bool
            If passed as False, will suppress error message printing to console.
        '''
        dt = yf.Ticker(symbol).history(period=period, interval=interval, start=start, end=end, prepost=prepost, debug=debug)

        return dt
    
    