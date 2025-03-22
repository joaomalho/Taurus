import warnings
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime
from bs4 import BeautifulSoup
from backend.funcionalities.formulas import Formulas

warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")

class DataHistoryYahoo():

    def __init__(self) -> None:
        self
    
    ########### STOCKS TOPs ###########
    def get_symbol_bio_info(self, symbol : str):
        '''
        Return detailed company information.
        '''
        
        try:
            yahoo_symbol_info = yf.Ticker(symbol).info
        except:
            yahoo_symbol_info = {}

        yahoo_symbol_about_info = {
                "LongName": yahoo_symbol_info.get("longName", "N/A"),
                "BusinessName": yahoo_symbol_info.get("longBusinessSummary", "N/A"),
                "Symbol": yahoo_symbol_info.get("symbol", "N/A"),
                "City": yahoo_symbol_info.get("city", "N/A"),
                "State": yahoo_symbol_info.get("state", "N/A"),
                "ZipCode": yahoo_symbol_info.get("zip", "N/A"),
                "Country": yahoo_symbol_info.get("country", "N/A"),
                "Sector": yahoo_symbol_info.get("sector", "N/A"),
                "Industry": yahoo_symbol_info.get("industry", "N/A"),
                "Employees": yahoo_symbol_info.get("fullTimeEmployees", "N/A"),
                "Website": yahoo_symbol_info.get("website", "N/A"),
                "ReportWebsite": yahoo_symbol_info.get("irWebsite", "N/A"),
                "QuoteSource": yahoo_symbol_info.get("quoteSourceName", "N/A"),
                "QuoteType": yahoo_symbol_info.get("quoteType", "N/A"),
                "FinancialCurrency": yahoo_symbol_info.get("financialCurrency", "N/A"),
                "CurrentPrice": yahoo_symbol_info.get("currentPrice", "N/A"),
                "PreviousClose": yahoo_symbol_info.get("previousClose", "N/A"),
                "OpenPrice": yahoo_symbol_info.get("open", "N/A"),
        }

        return yahoo_symbol_about_info

    def get_stocks_gainers(self, table_class: str = None) -> pd.DataFrame:
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

    def get_stocks_most_active(self, table_class: str = None) -> pd.DataFrame:
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
            response = requests.get("https://finance.yahoo.com/markets/stocks/most-active/?start=0&count=100", headers=headers)
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
    
    def get_stocks_trending(self, table_class: str = None) -> pd.DataFrame:
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
            return df
        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

    def get_data_history(self, symbol : str, period : str, interval : str, start = '1900-01-01', end = datetime.now(), prepost : bool = True):
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
        yahoo_data_history.reset_index(inplace=True)

        yahoo_data_history["Date"] = yahoo_data_history["Date"].dt.strftime("%Y-%m-%d %H:%M")

        return yahoo_data_history

    def get_symbol_institutional_holders(self, symbol : str):
        '''
        Return the list of major institutional holders
        '''
        yahoo_symbol_institutional_holders = yf.Ticker(symbol).institutional_holders
        yahoo_symbol_institutional_holders['Date Reported'] = yahoo_symbol_institutional_holders['Date Reported'].dt.strftime("%Y-%m-%d %H:%M") 
        yahoo_symbol_institutional_holders['pctHeld'] = yahoo_symbol_institutional_holders['pctHeld']*100
        yahoo_symbol_institutional_holders['pctChange'] = yahoo_symbol_institutional_holders['pctChange']*100
        
        return yahoo_symbol_institutional_holders

    def get_symbol_recommendations(self, symbol : str):
        '''
        Return recommendations about asset
        '''
        yahoo_symbol_recommendations = yf.Ticker(symbol).recommendations
        current_date = datetime.now()  # Obtém a data atual
        yahoo_symbol_recommendations["period"] = yahoo_symbol_recommendations.index.map(
            lambda x: (current_date - pd.DateOffset(months=x)).strftime("%B/%Y")  # Nome do mês + ano
        )
        return yahoo_symbol_recommendations

    def get_sector_etf_info(self, sector : str, search_value : str = "info"):
        """
        Return information about symbol ETF sector.
        """
        sector_map = {
            "Technology": "XLK",
            "Financial Services": "XLF",
            "Consumer Cyclical": "XLY",
            "Healthcare": "XLV",
            "Communication Services": "XLC",
            "Industrials": "XLI",
            "Consumer Defensive": "XLP",
            "Energy": "XLE",
            "Real Estate": "XLRE",
            "Basic Materials": "XLB",
            "Utilities": "XLU",
        }

        etf_symbol = sector_map.get(sector)
        if not etf_symbol:
            return "N/A"

        ticker = yf.Ticker(etf_symbol)

        if search_value == "info":
            return ticker.info
        else:
            return ticker.info.get(search_value, "N/A")
   
    def get_symbol_fundamental_info(self, symbol : str):
        '''
        Return detailed fundamental information about asset
        '''
        try:
            yahoo_symbol_info = yf.Ticker(symbol).info
        except:
            yahoo_symbol_info = {}
        try:
            yahoo_symbol_balancesheet = yf.Ticker(symbol).balance_sheet
        except:
            yahoo_symbol_balancesheet = pd.DataFrame()
        try:
            yahoo_symbol_income = yf.Ticker(symbol).income_stmt
        except:
            yahoo_symbol_income = pd.DataFrame()
        try:
            yahoo_symbol_cashflow = yf.Ticker(symbol).cash_flow
        except:
            yahoo_symbol_cashflow = pd.DataFrame()
        
        # Valuation
        sector = yahoo_symbol_info.get("sector")
        dh = DataHistoryYahoo()
        sector_pe = dh.get_sector_etf_info(sector, "trailingPE")

        # Dividends & BuyBacks
        eps_ann = yahoo_symbol_info.get("epsCurrentYear", "N/A")
        dividend_rate = yahoo_symbol_info.get("dividendRate", "N/A")
        if eps_ann != "N/A" and dividend_rate != "N/A":
            div_coverage_rate = eps_ann / dividend_rate if dividend_rate != 0 else "N/A"
        else:
            div_coverage_rate = "N/A" 

        # Profitability
        # net_income
        if 'Net Income' in yahoo_symbol_income.index:
            net_income = yahoo_symbol_income.loc['Net Income']
            if pd.isna(net_income).all():
                net_income = "N/A"

        # total_revenue
        if 'Total Revenue' in yahoo_symbol_income.index:
            total_revenue = yahoo_symbol_income.loc['Total Revenue']
            if pd.isna(total_revenue).all():
                total_revenue = "N/A"

        # cost_of_revenue
        if 'Cost Of Revenue' in yahoo_symbol_income.index:
            cost_of_revenue = yahoo_symbol_income.loc['Cost Of Revenue']
            if pd.isna(cost_of_revenue).all():
                cost_of_revenue = "N/A"

        # gross_profit
        if 'Gross Profit' in yahoo_symbol_income.index:
            gross_profit = yahoo_symbol_income.loc['Gross Profit']
            if pd.isna(gross_profit).all():
                gross_profit = "N/A"

        # operating_expenses
        if 'Operating Expense' in yahoo_symbol_income.index:
            operating_expenses = yahoo_symbol_income.loc['Operating Expense']
            if pd.isna(operating_expenses).all():
                operating_expenses = "N/A"
                    
        fm = Formulas()
        
        yoy_cost_of_revenue = fm.get_yoy_metric(cost_of_revenue)
        yoy_total_revenue = fm.get_yoy_metric(total_revenue)
        yoy_operating_expenses = fm.get_yoy_metric(operating_expenses)

        cagr_cost_of_revenue = fm.get_cagr_metric(cost_of_revenue)
        cagr_total_revenue = fm.get_cagr_metric(total_revenue)
        cagr_operating_expenses = fm.get_cagr_metric(operating_expenses)

        # Growth & NetWorth & Health
        # total_assets
        if 'Total Assets' in yahoo_symbol_balancesheet.index:
            total_assets = yahoo_symbol_balancesheet.loc['Total Assets']
            if pd.isna(total_assets).all():
                total_assets = "N/A"
        
        # current_liabilities
        if 'Current Liabilities' in yahoo_symbol_balancesheet.index:
            current_liabilities = yahoo_symbol_balancesheet.loc['Current Liabilities']
            if pd.isna(current_liabilities).all():
                current_liabilities = "N/A"

        # non_current_liabilities
        if 'Total Non Current Liabilities Net Minority Interest' in yahoo_symbol_balancesheet.index:
            non_current_liabilities = yahoo_symbol_balancesheet.loc['Total Non Current Liabilities Net Minority Interest']
            if pd.isna(non_current_liabilities).all():
                non_current_liabilities = "N/A"

        # total_liabilities
        if current_liabilities.iloc[0] != "N/A" and non_current_liabilities.iloc[0] != "N/A":
            total_liabilities = current_liabilities + non_current_liabilities
        else:
            total_liabilities = "N/A"

        # net_worth
        if total_assets.iloc[0] != "N/A" and current_liabilities.iloc[0] != "N/A" and non_current_liabilities.iloc[0] != "N/A":
            net_worth = total_assets.iloc[0] - total_liabilities.iloc[0]
        else:
            net_worth = "N/A"

        # current_assets
        if 'Current Assets' in yahoo_symbol_balancesheet.index:
            current_assets = yahoo_symbol_balancesheet.loc['Current Assets']
            if pd.isna(current_assets).all():
                current_assets = "N/A"

        # non_current_assets
        if 'Total Non Current Assets' in yahoo_symbol_balancesheet.index:
            non_current_assets = yahoo_symbol_balancesheet.loc['Total Non Current Assets']
            if pd.isna(non_current_assets).all():
                non_current_assets = "N/A"
        
        # short_term_debt_coverage
        if current_assets.iloc[0] != "N/A" and current_liabilities.iloc[0] != "N/A":
            short_term_debt_coverage = current_assets - current_liabilities
        else:
            short_term_debt_coverage = "N/A"

        # long_term_debt_coverage
        if non_current_assets.iloc[0] != "N/A" and non_current_liabilities.iloc[0] != "N/A":
            long_term_debt_coverage = non_current_assets - non_current_liabilities
        else:
            long_term_debt_coverage = "N/A"

        cagr_total_liabilities = fm.get_cagr_metric(total_liabilities)
        cagr_total_assets = fm.get_cagr_metric(total_assets)

        # cash_cash_equivalents
        if 'Cash And Cash Equivalents' in yahoo_symbol_balancesheet.index:
            cash_cash_equivalents = yahoo_symbol_balancesheet.loc['Cash And Cash Equivalents']
            if pd.isna(cash_cash_equivalents).all():
                cash_cash_equivalents = "N/A"

        # stockholders_equity
        if 'Stockholders Equity' in yahoo_symbol_balancesheet.index:
            stockholders_equity = yahoo_symbol_balancesheet.loc['Stockholders Equity']
            if pd.isna(stockholders_equity).all():
                stockholders_equity = "N/A"
        
        cagr_stockholder_equity = fm.get_cagr_metric(stockholders_equity)
        
        # Cashflow
        # free_cashflow
        if 'Free Cash Flow' in yahoo_symbol_cashflow.index:
            free_cashflow = yahoo_symbol_cashflow.loc['Free Cash Flow']
            if pd.isna(free_cashflow).all():
                free_cashflow = "N/A"
        
        # operating_cashflow
        if 'Operating Cash Flow' in yahoo_symbol_cashflow.index:
            operating_cashflow = yahoo_symbol_cashflow.loc['Operating Cash Flow']
            if pd.isna(operating_cashflow).all():
                operating_cashflow = "N/A"

        # capital_expenditure
        if 'Capital Expenditure' in yahoo_symbol_cashflow.index:
            capital_expenditure = yahoo_symbol_cashflow.loc['Capital Expenditure']
            if pd.isna(capital_expenditure).all():
                capital_expenditure = "N/A"

        # market_cap
        market_cap = yahoo_symbol_info.get('marketCap', "N/A")

        # free_cashflow_yield
        if market_cap != "N/A" and free_cashflow.iloc[0] != "N/A":
            free_cashflow_yield = (free_cashflow.iloc[0] / market_cap) * 100
        else:
            free_cashflow_yield = "N/A"

        # Ratios
        # current_ratio
        if current_assets.iloc[0] != "N/A" and current_liabilities.iloc[0] != "N/A":
            current_ratio = (current_assets / current_liabilities) * 100
        else:
            current_ratio = "N/A"
        
        # cagr_current_ratio
        cagr_current_ratio = fm.get_cagr_metric(current_ratio)
        
        # cash_ratio
        if cash_cash_equivalents.iloc[0] != "N/A" and current_liabilities.iloc[0] != "N/A":
            cash_ratio = (cash_cash_equivalents / current_liabilities) * 100
        else:
            cash_ratio = "N/A"
        
        # cagr_cash_ratio
        cagr_cash_ratio = fm.get_cagr_metric(cash_ratio)

        # gross_margin
        if gross_profit.iloc[0] != "N/A" and total_revenue.iloc[0] != "N/A":
            gross_margin = (gross_profit / total_revenue ) * 100
        else:
            gross_margin = "N/A"

        # cagr_gross_margin
        # cagr_gross_margin = fm.get_cagr_metric(gross_margin)

        # operating_income
        if 'Operating Income' in yahoo_symbol_income.index:
            operating_income = yahoo_symbol_income.loc['Operating Income']
            if pd.isna(operating_income).all():
                operating_income = "N/A"

        # operation_margin
        if operating_income.iloc[0] != "N/A" and total_revenue.iloc[0] != "N/A":
            operating_margin = (operating_income / total_revenue ) * 100
        else:
            operating_margin = "N/A"

        # cagr_operating_margin
        cagr_operating_margin = fm.get_cagr_metric(operating_margin)

        # profit_margin
        if net_income.iloc[0] != "N/A" and total_revenue.iloc[0] != "N/A":
            profit_margin = (net_income / total_revenue) * 100
        else:
            profit_margin = "N/A"

        # cagr_profit_margin
        cagr_profit_margin = fm.get_cagr_metric(profit_margin)
        
        # return_on_equity
        if net_income.iloc[0] != "N/A" and stockholders_equity.iloc[0] != "N/A":
            return_on_equity = (net_income / stockholders_equity) * 100
        else:
            return_on_equity = "N/A"

        # cagr_return_on_equity
        cagr_return_on_equity = fm.get_cagr_metric(return_on_equity)
        
        yahoo_symbol_fundamental_info = {
            "valuation": {
                "trailingPE": yahoo_symbol_info.get("trailingPE", "N/A"),
                "sectorTrailingPE": sector_pe,
                "forwardPE": yahoo_symbol_info.get("forwardPE", "N/A"),
                "PEGRatio": yahoo_symbol_info.get("trailingPegRatio", "N/A"),
            },
            "dividends": {
                "divCoverageRate": div_coverage_rate,
                "dividendYield": yahoo_symbol_info.get("dividendYield", "N/A"),
                "fiveYearAvgDividendYield": yahoo_symbol_info.get("fiveYearAvgDividendYield", "N/A"),
            },
            "profitability": {
                "NetIncome": net_income.iloc[0],
                "TotalRevenue": total_revenue.iloc[0],
                "CostOfRevenue": cost_of_revenue.iloc[0],
                "GrossProfit": gross_profit.iloc[0],
                "OperatingExpenses": operating_expenses.iloc[0],
                "CostOfRevenueCAGR": cagr_cost_of_revenue,
                "TotalRevenueCAGR": cagr_total_revenue,
                "OperatingExpensesCAGR": cagr_operating_expenses,
                # "CostOfRevenueYOY": yoy_cost_of_revenue,
                # "TotalRevenueYOY": yoy_total_revenue,
            },
            "liquidity": {
                # Actual
                "TotalAssets": total_assets.iloc[0],
                "TotalLiabilities": total_liabilities.iloc[0],
                "NetWorth": net_worth,
                "CashCashEquivalents": cash_cash_equivalents.iloc[0],
                # Short Term 1y
                "ShortTermDebtCoverage" : short_term_debt_coverage.iloc[0],
                "CurrentAssets": current_assets.iloc[0],
                "CurrentLiabilities": current_liabilities.iloc[0],
                # Long Term
                "LongTermDebtCoverage" : long_term_debt_coverage.iloc[0],
                "NonCurrentAssets": non_current_assets.iloc[0],
                "NonCurrentLiabilities": non_current_liabilities.iloc[0],
                # Growth
                "TotalAssetsCAGR": cagr_total_assets,
                "TotalLiabilitiesCAGR": cagr_total_liabilities,
                # Stockholders Equity
                "StockholdersEquityCAGR": cagr_stockholder_equity,
                "StockholdersEquity": stockholders_equity.iloc[0],
            },
            "cashflow": {
                "FreeCashflow": free_cashflow.iloc[0],
                "OperatingCashflow": operating_cashflow.iloc[0],
                "CapitalExpenditure": capital_expenditure.iloc[0],
                "MarketCap": market_cap,
                "FreeCashflowYield": free_cashflow_yield,
            },
            "ratios": {
                # Health & Debt
                "CurrentRatio": current_ratio.iloc[0],
                "CurrentRatioCAGR": cagr_current_ratio,
                "CashRatio": cash_ratio.iloc[0],
                "CashRatioCAGR": cagr_cash_ratio,
                # Margins
                "GrossMargin": gross_margin.iloc[0],
                # "GrossMarginCAGR": cagr_gross_margin,
                "OperatingMargin": operating_margin.iloc[0],
                "OperatingMarginCAGR": cagr_operating_margin,
                "ProfitMargin": profit_margin.iloc[0],
                "ProfitMarginCAGR": cagr_profit_margin,
                "ReturnOnEquity": return_on_equity.iloc[0],
                "ReturnOnEquityCAGR": cagr_return_on_equity,
            },
            "market_risk_and_sentiment": {
                "beta": yahoo_symbol_info.get("beta", "N/A"),
                "auditRisk": yahoo_symbol_info.get("auditRisk", "N/A"),
                "boardRisk": yahoo_symbol_info.get("boardRisk", "N/A"),
                "sharesPercentSharesOut": yahoo_symbol_info.get("sharesPercentSharesOut", "N/A"),
                "recommendationMean": yahoo_symbol_info.get("recommendationMean", "N/A"),
                "targetMeanPrice": yahoo_symbol_info.get("targetMeanPrice", "N/A")
            }
        }
        return yahoo_symbol_fundamental_info


   ########### FOREX ###########   
    ##### NOT IN USE ##### 
    
    def get_yahoo_symbol_dividends(self, symbol : str):
        '''
        Return dividents historics
        '''
        yahoo_symbol_dividends = yf.Ticker(symbol).dividends
        return yahoo_symbol_dividends
    
    def get_yahoo_symbol_splits(self, symbol : str):
        '''
        Return actions splits historics
        '''
        yahoo_symbol_splits = yf.Ticker(symbol).splits
        return yahoo_symbol_splits
 
 
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

    
    ########### WORLD INDICES ###########
    def get_yahoo_indices(self, table_class: str = None) -> pd.DataFrame:
        """
        Extrat data from yahoo world indices.

        Parameters:
            classe_tabela (str): Class CSS from table to scrap (optional).

        Returns:
            pd.DataFrame: DataFrame with table content.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get("https://finance.yahoo.com/markets/world-indices/", headers=headers)
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
            df["Change %"] = df["Change %"].str.replace("%", "", regex=False).str.replace("+", "", regex=False)
            df["Volume"] = df["Volume"].str.replace("-", "0", regex=False)
            df.drop(columns=["52 Wk Range", "Day Range"], inplace=True)
            
        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")
    
        return df

    ########### CRYPTOS ###########
    def get_yahoo_crypto_top100_gainers(self, table_class: str = None) -> pd.DataFrame:
        """
        Extrat data from yahoo crypto top 100 gainers

        Parameters:
            classe_tabela (str): Class CSS from table to scrap (optional).

        Returns:
            pd.DataFrame: DataFrame with table content.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get("https://finance.yahoo.com/markets/crypto/gainers/?start=0&count=100", headers=headers)
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
            df["Change %"] = df["Change %"].str.replace("%", "", regex=False).str.replace("+", "", regex=False)
            df["Volume"] = df["Volume"].str.replace("-", "0", regex=False)
            df["Volume In Currency (24hr)"] = df["Volume In Currency (24hr)"].str.replace("-", "0", regex=False)
            df["Total Volume All Currencies (24hr)"] = df["Total Volume All Currencies (24hr)"].str.replace("-", "0", regex=False)
            df["52 Wk Change %"] = df["52 Wk Change %"].str.replace("%", "", regex=False)
            df.drop(columns=["52 Wk Range"], inplace=True)
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

        return df

    def get_yahoo_crypto_top100_most_active(self, table_class: str = None) -> pd.DataFrame:
        """
        Extrat data from yahoo crypto top 100 most active.

        Parameters:
            classe_tabela (str): Class CSS from table to scrap (optional).

        Returns:
            pd.DataFrame: DataFrame with table content.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get("https://finance.yahoo.com/markets/crypto/most-active/?start=0&count=100", headers=headers)
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
            df["Change %"] = df["Change %"].str.replace("%", "", regex=False).str.replace("+", "", regex=False)
            df["Volume"] = df["Volume"].str.replace("-", "0", regex=False)
            df["Volume In Currency (24hr)"] = df["Volume In Currency (24hr)"].str.replace("-", "0", regex=False)
            df["Total Volume All Currencies (24hr)"] = df["Total Volume All Currencies (24hr)"].str.replace("-", "0", regex=False)
            df["52 Wk Change %"] = df["52 Wk Change %"].str.replace("%", "", regex=False)
            df.drop(columns=["52 Wk Range"], inplace=True)
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

        return df

    def get_yahoo_crypto_trending(self, table_class: str = None) -> pd.DataFrame:
        """
        Extrat data from yahoo trending cryptos.

        Parameters:
            classe_tabela (str): Class CSS from table to scrap (optional).

        Returns:
            pd.DataFrame: DataFrame with table content.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get("https://finance.yahoo.com/markets/crypto/trending/", headers=headers)
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
            df["Change %"] = df["Change %"].str.replace("%", "", regex=False).str.replace("+", "", regex=False)
            df["Market Cap"] = df["Market Cap"].str.replace("-", "0", regex=False)
            df["Volume"] = df["Volume"].str.replace("-", "0", regex=False)
            df["Volume In Currency (24hr)"] = df["Volume In Currency (24hr)"].str.replace("-", "0", regex=False)
            df["Total Volume All Currencies (24hr)"] = df["Total Volume All Currencies (24hr)"].str.replace("-", "0", regex=False)
            df["52 Wk Change %"] = df["52 Wk Change %"].str.replace("%", "", regex=False).str.replace("-", "0", regex=False)
            df.drop(columns=["52 Wk Range"], inplace=True)

        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

        return df
    