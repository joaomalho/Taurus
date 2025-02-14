import warnings
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")

class DataHistoryYahoo():

    def __init__(self) -> None:
        self
    
    def get_yahoo_top100_gainers(table_class: str = None) -> pd.DataFrame:
        """
        Extrat data from yahoo top 100 gainers

        Parameters:
            classe_tabela (str): Class CSS from table to scrap (optional).

        Returns:
            pd.DataFrame: DataFrame with table content.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get("https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=100", headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            if table_class:
                tabela = soup.find('table', {'class': table_class})
            else:
                tabela = soup.find('table')

            headers = [th.text.strip() for th in tabela.find_all('th')]

            rows = []
            for row in tabela.find_all('tr')[1:]:
                cols = [td.text.strip() for td in row.find_all('td')]
                if cols: 
                    rows.append(cols)

            df = pd.DataFrame(rows, columns=headers if headers else None)
            df["Price"] = df["Price"].str.extract(r"^([\d\.]+)")
            df["Change"] = df["Change"].str.replace("+", "", regex=False)
            df["Change %"] = df["Change %"].str.replace("%", "", regex=False)
            df["Volume"] = df["Volume"].str.replace("-", "0", regex=False)
            df["Avg Vol (3M)"] = df["Avg Vol (3M)"].str.replace("-", "0", regex=False)
            df["Market Cap"] = df["Market Cap"].str.replace("-", "0", regex=False)
            df["P/E Ratio (TTM)"] = df["P/E Ratio (TTM)"].str.replace("-", "0", regex=False)
            df["52 Wk Change %"] = df["52 Wk Change %"].str.replace("%", "", regex=False)
            df.drop(columns=["52 Wk Range"], inplace=True)
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

        return df


    def get_yahoo_most_active(self, table_class: str = None) -> pd.DataFrame:
        """
        Extrat data from yahoo most active

        Parameters:
            classe_tabela (str): Class CSS from table to scrap (optional).

        Returns:
            pd.DataFrame: DataFrame with table content.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get("https://finance.yahoo.com/markets/stocks/most-active/", headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            if table_class:
                tabela = soup.find('table', {'class': table_class})
            else:
                tabela = soup.find('table')

            headers = [th.text.strip() for th in tabela.find_all('th')]

            rows = []
            for row in tabela.find_all('tr')[1:]:
                cols = [td.text.strip() for td in row.find_all('td')]
                if cols: 
                    rows.append(cols)

            df = pd.DataFrame(rows, columns=headers if headers else None)
            df["Price"] = df["Price"].str.extract(r"^([\d\.]+)")
            df["Change"] = df["Change"].str.replace("+", "", regex=False)
            df["Change %"] = df["Change %"].str.replace("%", "", regex=False)
            df["P/E Ratio (TTM)"] = df["P/E Ratio (TTM)"].str.replace("-", "0", regex=False)
            df["52 Wk Change %"] = df["52 Wk Change %"].str.replace("%", "", regex=False)
            df.drop(columns=["52 Wk Range"], inplace=True)
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")
    
        return df
    
    def get_yahoo_trending(table_class: str = None) -> pd.DataFrame:
        """
        Extrat data from yahoo trending.

        Parameters:
            classe_tabela (str): Class CSS from table to scrap (optional).

        Returns:
            pd.DataFrame: DataFrame with table content.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get("https://finance.yahoo.com/markets/stocks/trending/", headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            if table_class:
                tabela = soup.find('table', {'class': table_class})
            else:
                tabela = soup.find('table')

            headers = [th.text.strip() for th in tabela.find_all('th')]

            rows = []
            for row in tabela.find_all('tr')[1:]:
                cols = [td.text.strip() for td in row.find_all('td')]
                if cols: 
                    rows.append(cols)

            df = pd.DataFrame(rows, columns=headers if headers else None)
            df["Price"] = df["Price"].str.extract(r"^([\d\.]+)")
            df["Change"] = df["Change"].str.replace("+", "", regex=False)
            df["Change %"] = df["Change %"].str.replace("%", "", regex=False)
            df["Avg Vol (3M)"] = df["Avg Vol (3M)"].str.replace("-", "0", regex=False)
            df["Market Cap"] = df["Market Cap"].str.replace("-", "0", regex=False)
            df["P/E Ratio (TTM)"] = df["P/E Ratio (TTM)"].str.replace("-", "0", regex=False)
            df["52 Wk Change %"] = df["52 Wk Change %"].str.replace("%", "", regex=False)
            df.drop(columns=["52 Wk Range"], inplace=True)

        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

        return df


    def get_yahoo_data_history(self, symbol : str, period : str, interval : str, start = '1900-01-01', end = datetime.now(), prepost : bool = True):
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
        '''
        yahoo_data_history = yf.Ticker(symbol).history(period=period, interval=interval, start=start, end=end, prepost=prepost)
        return yahoo_data_history
    
    def get_yahoo_symbol_info(self, symbol : str):
        '''
        Return detailed information about asset
        '''
        yahoo_symbol_info = yf.Ticker(symbol).info
        return yahoo_symbol_info
    
    def get_yahoo_symbol_dividends(self, symbol : str):
        '''
        Return dividents historics
        '''
        yahoo_symbol_dividends = yf.Ticker(symbol).divwidends
        return yahoo_symbol_dividends
    
    def get_yahoo_symbol_splits(self, symbol : str):
        '''
        Return actions splits historics
        '''
        yahoo_symbol_splits = yf.Ticker(symbol).splits
        return yahoo_symbol_splits
 
    def get_yahoo_symbol_recommendations(self, symbol : str):
        '''
        Return recommendations about asset
        '''
        yahoo_symbol_recommendations = yf.Ticker(symbol).recommendations
        return yahoo_symbol_recommendations

    def get_yahoo_symbol_calendar(self, symbol : str):
        '''
        Return corporative calendar events about asset
        '''
        yahoo_symbol_calendar = yf.Ticker(symbol).calendar
        return yahoo_symbol_calendar

    def get_yahoo_symbol_major_holders(self, symbol : str):
        '''
        Return the list of major holders
        '''
        yahoo_symbol_major_holders = yf.Ticker(symbol).major_holders
        return yahoo_symbol_major_holders

    def get_yahoo_symbol_institutional_holders(self, symbol : str):
        '''
        Return the list of major institutional holders
        '''
        yahoo_symbol_institutional_holders = yf.Ticker(symbol).institutional_holders
        return yahoo_symbol_institutional_holders

    def get_yahoo_symbol_balance_sheet(self, symbol : str):
        '''
        Return the patrimonial balance sheet
        '''
        yahoo_symbol_balance_sheet = yf.Ticker(symbol).balance_sheet
        return yahoo_symbol_balance_sheet

    def get_yahoo_symbol_financials(self, symbol : str):
        '''
        !!! Not Working !!!
        Return the financials results (profits and expenses)
        '''
        yahoo_symbol_financials = yf.Ticker(symbol).financials
        return yahoo_symbol_financials

    def get_yahoo_symbol_cashflow(self, symbol : str):
        '''
        Return the cashflow results
        '''
        yahoo_symbol_cashflow = yf.Ticker(symbol).cashflow
        return yahoo_symbol_cashflow

    def get_yahoo_symbol_sustainability(self, symbol : str):
        '''
        
        Return the ESG metrics (enviormental, social and governamental)
        '''
        yahoo_symbol_sustainability = yf.Ticker(symbol).sustainability
        return yahoo_symbol_sustainability

    def get_yahoo_symbol_news(self, symbol : str):
        '''
        Return the latest news about asset
        '''
        yahoo_symbol_news = yf.Ticker(symbol).news
        return yahoo_symbol_news

    def get_yahoo_symbol_fast_info(self, symbol : str):
        '''
        Return the fast information about asset

        Data:
        exchange : str
            Exchange on which the asset is traded
        marketCap : float
            Marker Cap of asset
        quoteType: str
            Asset type (EQUITY, CRYPTO, FOREX..)
        shares : int
            Total Number of shares in circulation            
        '''
        yahoo_symbol_fast_info_exchange = yf.Ticker(symbol).fast_info.exchange
        yahoo_symbol_fast_info_marketcap = yf.Ticker(symbol).fast_info.market_cap
        yahoo_symbol_fast_info_quotetype = yf.Ticker(symbol).fast_info.quote_type
        yahoo_symbol_fast_info_shares = yf.Ticker(symbol).fast_info.shares
        return yahoo_symbol_fast_info_exchange, yahoo_symbol_fast_info_marketcap, yahoo_symbol_fast_info_quotetype, yahoo_symbol_fast_info_shares
    


