import math
import warnings
import requests
# import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from bs4 import BeautifulSoup
from backend.funcionalities.formulas import Formulas

warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")


class DataHistoryYahoo():

    def __init__(self) -> None:
        self

    # ---------- STOCKS TOPs ----------
    def get_symbol_bio_info(self, symbol: str):
        '''
        Return detailed company information.
        '''

        try:
            yahoo_symbol_info = yf.Ticker(symbol).info
        except Exception:
            yahoo_symbol_info = {}

        adv_3m = yahoo_symbol_info.get("averageDailyVolume3Month")
        out = yahoo_symbol_info.get("sharesOutstanding")
        turnover_year_out = (adv_3m * 252)/out if adv_3m is not None else "N/A"
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
                "Beta": yahoo_symbol_info.get("beta", "N/A"),
                "ShareTurnover": turnover_year_out,
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

            fm = Formulas()

            df = pd.DataFrame(rows, columns=headers if headers else None)
            df["Price"] = pd.to_numeric(df["Price"].str.extract(r"^([\d\.]+)")[0], errors="coerce").fillna(0).round(2)
            df["Change"] = pd.to_numeric(df["Change"].str.replace(r"^\+", "", regex=True), errors='coerce').fillna(0).round(2)
            df["Change %"] = pd.to_numeric(df["Change %"].str.replace("%", "", regex=False), errors='coerce').fillna(0).round(2)
            df["Volume"] = pd.to_numeric(df["Volume"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["Avg Vol (3M)"] = pd.to_numeric(df["Avg Vol (3M)"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["Market Cap"] = pd.to_numeric(df["Market Cap"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["P/E Ratio (TTM)"] = pd.to_numeric(df["P/E Ratio (TTM)"].str.replace("-", "0", regex=False), errors='coerce').fillna(0).round(2)
            df["52 Wk Change %"] = pd.to_numeric(df["52 Wk Change %"].str.replace("%", "", regex=False), errors='coerce').fillna(0).round(2)
            df.drop(columns=["52 Wk Range"], inplace=True)
            df.drop(columns=[""], inplace=True)

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

            fm = Formulas()

            df = pd.DataFrame(rows, columns=headers if headers else None)
            df["Price"] = pd.to_numeric(df["Price"].str.extract(r"^([\d\.]+)")[0], errors="coerce").fillna(0).round(2)
            df["Change"] = pd.to_numeric(df["Change"].str.replace(r"^\+", "", regex=True), errors='coerce').fillna(0).round(2)
            df["Change %"] = pd.to_numeric(df["Change %"].str.replace("%", "", regex=False), errors='coerce').fillna(0).round(2)
            df["Volume"] = pd.to_numeric(df["Volume"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["Avg Vol (3M)"] = pd.to_numeric(df["Avg Vol (3M)"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["Market Cap"] = pd.to_numeric(df["Market Cap"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["P/E Ratio (TTM)"] = pd.to_numeric(df["P/E Ratio (TTM)"].str.replace("-", "0", regex=False), errors='coerce').fillna(0).round(2)
            df["52 Wk Change %"] = pd.to_numeric(df["52 Wk Change %"].str.replace("%", "", regex=False), errors='coerce').fillna(0).round(2)
            df.drop(columns=["52 Wk Range"], inplace=True)
            df.drop(columns=[""], inplace=True)
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

            fm = Formulas()

            df = pd.DataFrame(rows, columns=headers if headers else None)
            df["Price"] = pd.to_numeric(df["Price"].str.extract(r"^([\d\.]+)")[0], errors="coerce").fillna(0).round(2)
            df["Change"] = pd.to_numeric(df["Change"].str.replace(r"^\+", "", regex=True), errors='coerce').fillna(0).round(2)
            df["Change %"] = pd.to_numeric(df["Change %"].str.replace("%", "", regex=False), errors='coerce').fillna(0).round(2)
            df["Volume"] = pd.to_numeric(df["Volume"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["Avg Vol (3M)"] = pd.to_numeric(df["Avg Vol (3M)"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["Market Cap"] = pd.to_numeric(df["Market Cap"].str.replace("-", "0", regex=False).apply(fm.convert_string_milions), errors='coerce')
            df["P/E Ratio (TTM)"] = pd.to_numeric(df["P/E Ratio (TTM)"].str.replace("-", "0", regex=False), errors='coerce').fillna(0).round(2)
            df["52 Wk Change %"] = pd.to_numeric(df["52 Wk Change %"].str.replace("%", "", regex=False), errors='coerce').fillna(0).round(2)
            df.drop(columns=["52 Wk Range"], inplace=True)
            df.drop(columns=[""], inplace=True)
            return df
        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

    def get_data_history(self, symbol: str, period: str, interval: str, start='1900-01-01', end=datetime.now(), prepost: bool = True):
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
        yahoo_data_history = yf.Ticker(symbol).history(period=period, interval=interval, prepost=prepost)
        yahoo_data_history.reset_index(inplace=True)

        yahoo_data_history["Date"] = yahoo_data_history["Date"].dt.strftime("%Y-%m-%d %H:%M")

        return yahoo_data_history

    def get_symbol_institutional_holders(self, symbol: str):
        '''
        Return the list of major institutional holders
        '''
        yahoo_symbol_institutional_holders = yf.Ticker(symbol).institutional_holders
        yahoo_symbol_institutional_holders['Date Reported'] = yahoo_symbol_institutional_holders['Date Reported'].dt.strftime("%Y-%m-%d %H:%M")
        yahoo_symbol_institutional_holders['pctHeld'] = yahoo_symbol_institutional_holders['pctHeld']*100
        yahoo_symbol_institutional_holders['pctChange'] = yahoo_symbol_institutional_holders['pctChange']*100

        return yahoo_symbol_institutional_holders

    def get_symbol_recommendations(self, symbol: str):
        '''
        Return recommendations about asset
        '''
        yahoo_symbol_recommendations = yf.Ticker(symbol).recommendations
        current_date = datetime.now()  # Obtém a data atual
        yahoo_symbol_recommendations["period"] = yahoo_symbol_recommendations.index.map(
            lambda x: (current_date - pd.DateOffset(months=x)).strftime("%B/%Y")  # Nome do mês + ano
        )
        return yahoo_symbol_recommendations

    def get_sector_etf_info(self, sector: str, search_value: str = "info"):
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

    def get_symbol_fundamental_info(self, symbol: str):
        '''
        Return detailed fundamental information about asset
        '''
        try:
            yahoo_symbol_info = yf.Ticker(symbol).info
        except Exception:
            yahoo_symbol_info = {}
        try:
            yahoo_symbol_balancesheet = yf.Ticker(symbol).balance_sheet
        except Exception:
            yahoo_symbol_balancesheet = pd.DataFrame()
        try:
            yahoo_symbol_balancesheet_quarter = yf.Ticker(symbol).quarterly_balance_sheet
        except Exception:
            yahoo_symbol_balancesheet_quarter = pd.DataFrame()
        try:
            yahoo_symbol_income = yf.Ticker(symbol).income_stmt
        except Exception:
            yahoo_symbol_income = pd.DataFrame()
        try:
            yahoo_symbol_income_quarter = yf.Ticker(symbol).quarterly_income_stmt
        except Exception:
            yahoo_symbol_income_quarter = pd.DataFrame()
        # try:
        #     yahoo_symbol_cashflow = yf.Ticker(symbol).cash_flow
        # except Exception:
        #     yahoo_symbol_cashflow = pd.DataFrame()
        try:
            yahoo_symbol_cashflow_quarter = yf.Ticker(symbol).quarterly_cash_flow
        except Exception:
            yahoo_symbol_cashflow_quarter = pd.DataFrame()
        try:
            yahoo_symbol_dividends = yf.Ticker(symbol).dividends
        except Exception:
            yahoo_symbol_dividends = pd.Series(dtype=float)

        fm = Formulas()
        # ------ Valuation ------ #
        # - Price Earnings
        sector = yahoo_symbol_info.get("sector")
        sector_pe = self.get_sector_etf_info(sector, "trailingPE")

        forward_pe = yahoo_symbol_info.get("forwardPE", None)
        trailing_pe = yahoo_symbol_info.get("trailingPE", None)

        # - Market Cap
        market_cap = yahoo_symbol_info.get('marketCap')
        if market_cap is None or (isinstance(market_cap, float) and math.isnan(market_cap)):
            market_cap = None

        # - Total Debt
        if 'Total Debt' in yahoo_symbol_balancesheet.index:
            total_debt = yahoo_symbol_balancesheet.loc["Total Debt"]
            if pd.isna(total_debt).all():
                total_debt = None
                total_debt_last = None
            else:
                total_debt = total_debt.dropna()
                total_debt_last = total_debt.iloc[0]
        else:
            total_ebitda = None
            total_debt_last = None

        # - Minority Interest
        if 'Total Equity Gross Minority Interest' in yahoo_symbol_balancesheet.index:
            total_equity_gross_minority_interest = yahoo_symbol_balancesheet.loc["Total Equity Gross Minority Interest"]
            if pd.isna(total_equity_gross_minority_interest).all():
                total_equity_gross_minority_interest = None
                total_equity_gross_minority_interest_last = None
            else:
                total_equity_gross_minority_interest = total_equity_gross_minority_interest.dropna()
                total_equity_gross_minority_interest_last = total_equity_gross_minority_interest.iloc[0]
        else:
            total_equity_gross_minority_interest = None
            total_equity_gross_minority_interest_last = None

        # - Stockholders Equity
        if 'Stockholders Equity' in yahoo_symbol_balancesheet.index:
            stockholders_equity = yahoo_symbol_balancesheet.loc["Stockholders Equity"]
            if pd.isna(stockholders_equity).all():
                stockholders_equity = None
                stockholders_equity_last = None
                stockholders_equity_mean = None
                last_stockholders_equity_mean = None
            else:
                stockholders_equity = stockholders_equity.dropna()
                stockholders_equity_last = stockholders_equity.iloc[0]
                stockholders_equity_mean = (stockholders_equity.shift(1) + stockholders_equity) / 2
                last_stockholders_equity_mean = stockholders_equity_mean.dropna().iloc[0]
        else:
            stockholders_equity = None
            stockholders_equity_last = None
            stockholders_equity_mean = None
            last_stockholders_equity_mean = None

        minority_interest = total_equity_gross_minority_interest_last - stockholders_equity_last \
            if stockholders_equity_last is not None \
            and total_equity_gross_minority_interest_last is not None \
            else None

        preferred_equity = 0  # incluir se tiver a rubrica

        # - Debt & cash (preferidos)
        if 'Cash Cash Equivalents And Short Term Investments' in yahoo_symbol_balancesheet.index:
            cash_sti = yahoo_symbol_balancesheet.loc["Cash Cash Equivalents And Short Term Investments"]
            if pd.isna(cash_sti).all():
                cash_sti = None
                cash_sti_last = None
            else:
                cash_sti = cash_sti.dropna()
                cash_sti_last = cash_sti.iloc[0]
        else:
            cash_sti = None
            cash_sti_last = None

        if cash_sti_last is None:
            if 'Cash And Cash Equivalents' in yahoo_symbol_balancesheet.index:
                cash = yahoo_symbol_balancesheet.loc["Cash And Cash Equivalents"]
                if pd.isna(cash).all():
                    cash = None
                    cash_last = None
                else:
                    cash = cash.dropna()
                    cash_last = cash.iloc[0]
            else:
                cash = None
                cash_last = None

            if 'Other Short Term Investments' in yahoo_symbol_balancesheet.index:
                sti = yahoo_symbol_balancesheet.loc["Other Short Term Investments"]
                if pd.isna(cash).all():
                    sti = None
                    sti_last = None
                else:
                    sti = sti.dropna()
                    sti_last = sti.iloc[0]
            else:
                sti = None
                sti_last = None

            cash_sti_last = (cash_last or 0) + (sti_last or 0) \
                if cash_last is not None \
                and sti_last is not None \
                else None

        # - Enterprise Value
        enterprise_value = market_cap + total_debt_last + minority_interest + preferred_equity - cash_sti_last \
            if market_cap is not None \
            and total_debt_last is not None \
            and minority_interest is not None \
            and preferred_equity is not None \
            and cash_sti_last is not None \
            else None

        # - Total Revenue ---- ADICIONAR ISTO em todo o lado e criar função generica
        if 'EBITDA' in yahoo_symbol_income_quarter.index:
            total_ebitda = yahoo_symbol_income_quarter.loc['EBITDA']
            if pd.isna(total_ebitda).all():
                total_ebitda = None
                ebitda_ttm = None
            else:
                total_ebitda = total_ebitda.dropna()
                ebitda_ttm = total_ebitda.sum()
        else:
            total_ebitda = None
            ebitda_ttm = None

        # - Total Revenue
        if 'Total Revenue' in yahoo_symbol_income_quarter.index:
            total_revenue = yahoo_symbol_income_quarter.loc['Total Revenue']
            if pd.isna(total_revenue).all():
                total_revenue = None
                total_revenue_last = None
                total_revenue_ttm = None
            else:
                total_revenue = total_revenue.dropna()
                total_revenue_last = total_revenue.iloc[0]
                total_revenue_ttm = total_revenue.sum()
        else:
            total_revenue = None
            total_revenue_last = None
            total_revenue_ttm = None

        # - Total Revenue FY
        if 'Total Revenue' in yahoo_symbol_income.index:
            total_revenue_fy = yahoo_symbol_income.loc['Total Revenue']
            if pd.isna(total_revenue_fy).all():
                total_revenue_fy = None
            else:
                total_revenue_fy = total_revenue_fy.dropna()
        else:
            total_revenue_fy = None

        # - Free Cashflow
        if 'Free Cash Flow' in yahoo_symbol_cashflow_quarter.index:
            free_cashflow = yahoo_symbol_cashflow_quarter.loc['Free Cash Flow']
            if pd.isna(free_cashflow).all():
                free_cashflow = None
                free_cashflow_ttm = None
            else:
                free_cashflow = free_cashflow.dropna()
                free_cashflow_ttm = free_cashflow.sum()
        else:
            free_cashflow = None
            free_cashflow_ttm = None

        # - Métricas
        ev_ebitda = enterprise_value / ebitda_ttm \
            if enterprise_value is not None \
            and ebitda_ttm not in (None, 0) \
            else None
        p_s = market_cap / total_revenue_ttm \
            if market_cap is not None \
            and total_revenue_ttm not in (None, 0) \
            else None
        fcf_yield_equity = free_cashflow_ttm / market_cap \
            if free_cashflow_ttm is not None \
            and market_cap not in (None, 0) \
            else None
        fcf_yield_enterp = free_cashflow_ttm / enterprise_value \
            if free_cashflow_ttm is not None \
            and enterprise_value not in (None, 0) \
            else None

        # ------ Finantial Health ------ #
        # - Net Debt / EBITDA
        net_debt = total_debt_last - cash_sti_last \
            if cash_sti_last is not None \
            and total_debt_last is not None \
            else None

        net_debt_ebitda = net_debt / ebitda_ttm \
            if net_debt is not None \
            and ebitda_ttm is not None \
            and ebitda_ttm > 0 \
            else None

        # - Interest Coverage (EBIT)
        if 'EBIT' in yahoo_symbol_income_quarter.index:
            ebit_quarter = yahoo_symbol_income_quarter.loc['EBIT']
            if pd.isna(ebit_quarter).all():
                ebit_quarter = None
                ebit_quarter_ttm = None
            else:
                ebit_quarter = ebit_quarter.dropna()
                ebit_quarter_ttm = ebit_quarter.sum()
        else:
            ebit_quarter = None
            ebit_quarter_ttm = None

        # - Interest Expense
        if 'Interest Expense' in yahoo_symbol_income.index:
            interest_expense = yahoo_symbol_income.loc['Interest Expense']
            if pd.isna(interest_expense).all():
                interest_expense = None
                interest_expense_ttm = None
                interest_expense_last = None
            else:
                interest_expense = interest_expense.dropna()
                interest_expense_ttm = interest_expense.sum()
                interest_expense_last = interest_expense.iloc[0]
        else:
            interest_expense = None
            interest_expense_ttm = None
            interest_expense_last = None

        interest_coverage_ebit = ebit_quarter_ttm / abs(interest_expense_ttm) \
            if ebit_quarter_ttm is not None \
            and interest_expense_ttm not in (None, 0) \
            else None

        # - Current Racio
        # current_assets
        if 'Current Assets' in yahoo_symbol_balancesheet_quarter.index:
            current_assets_quarter = yahoo_symbol_balancesheet_quarter.loc['Current Assets']
            if pd.isna(current_assets_quarter).all():
                current_assets_quarter = None
                current_assets_quarter_last = None
            else:
                current_assets_quarter = current_assets_quarter.dropna()
                current_assets_quarter_last = current_assets_quarter.iloc[0]
        else:
            current_assets_quarter = None
            current_assets_quarter_last = None

        # current_liabilities
        if 'Current Liabilities' in yahoo_symbol_balancesheet_quarter.index:
            current_liabilities_quarter = yahoo_symbol_balancesheet_quarter.loc['Current Liabilities']
            if pd.isna(current_liabilities_quarter).all():
                current_liabilities_quarter = None
                current_liabilities_quarter_last = None
            else:
                current_liabilities_quarter = current_liabilities_quarter.dropna()
                current_liabilities_quarter_last = current_liabilities_quarter.iloc[0]
        else:
            current_liabilities_quarter = None
            current_liabilities_quarter_last = None

        current_ratio = (current_assets_quarter_last / current_liabilities_quarter_last) \
            if current_liabilities_quarter_last not in (None, 0) \
            and current_assets_quarter_last is not None \
            else None

        # - Quick Racio
        # inventory
        if 'Inventory' in yahoo_symbol_balancesheet_quarter.index:
            inventory_quarter = yahoo_symbol_balancesheet_quarter.loc['Inventory']
            if pd.isna(inventory_quarter).all():
                inventory_quarter = None
                inventory_quarter_last = None
            else:
                inventory_quarter = inventory_quarter.dropna()
                inventory_quarter_last = inventory_quarter.iloc[0]
        else:
            inventory_quarter = None
            inventory_quarter_last = None

        quick_ratio = ((current_assets_quarter_last - inventory_quarter_last) / current_liabilities_quarter_last) \
            if current_assets_quarter_last is not None \
            and inventory_quarter_last is not None \
            and current_liabilities_quarter_last not in (None, 0) \
            else None

        # ------ Profitability ------ #
        # operation_margin
        operation_margin = ebit_quarter_ttm / total_revenue_ttm \
            if ebit_quarter_ttm is not None \
            and total_revenue_ttm not in (None, 0) \
            else None

        # fcf_margin
        fcf_margin = free_cashflow_ttm / total_revenue_ttm \
            if free_cashflow_ttm is not None \
            and total_revenue_ttm not in (None, 0) \
            else None

        # ROIC
        # Tax Rate For Calcs
        if 'Tax Rate For Calcs' in yahoo_symbol_income_quarter.index:
            tax_rate_quarter = yahoo_symbol_income_quarter.loc['Tax Rate For Calcs']
            if pd.isna(tax_rate_quarter).all():
                tax_rate_quarter = None
                tax_rate_ttm = None
            else:
                tax_rate_quarter = tax_rate_quarter.dropna()
                tax_rate_ttm = tax_rate_quarter.mean()
        else:
            tax_rate_quarter = None
            tax_rate_ttm = None

        # Invested Capital
        if 'Invested Capital' in yahoo_symbol_balancesheet.index:
            cap_invested = yahoo_symbol_balancesheet.loc['Invested Capital']
            if pd.isna(cap_invested).all():
                cap_invested = None
                cap_invested_mean = None
                last_capital = None
            else:
                cap_invested = cap_invested.dropna()
                cap_invested_mean = (cap_invested.shift(1) + cap_invested) / 2
                last_capital = cap_invested_mean.dropna().iloc[0]
        else:
            cap_invested = None
            cap_invested_mean = None
            last_capital = None

        nopat_ttm = (ebit_quarter_ttm * (1 - tax_rate_ttm)) \
            if ebit_quarter_ttm is not None \
            and tax_rate_ttm is not None \
            else None

        roic = nopat_ttm / last_capital \
            if nopat_ttm is not None \
            and last_capital is not None \
            else None

        # ROE
        # net_income_fy
        if 'Net Income' in yahoo_symbol_income.index:
            net_income_fy = yahoo_symbol_income.loc['Net Income']
            if pd.isna(net_income_fy).all():
                net_income_fy = None
            else:
                net_income_fy = net_income_fy.dropna()
        else:
            net_income_fy = None

        # net_income
        if 'Net Income' in yahoo_symbol_income_quarter.index:
            net_income_quarter = yahoo_symbol_income_quarter.loc['Net Income']
            if pd.isna(net_income_quarter).all():
                net_income_quarter = None
                net_income_ttm = None
            else:
                net_income_quarter = net_income_quarter.dropna()
                net_income_ttm = net_income_quarter.sum()
        else:
            net_income_quarter = None
            net_income_ttm = None

        roe = net_income_ttm / last_stockholders_equity_mean \
            if net_income_ttm is not None \
            and last_stockholders_equity_mean not in (None,0) \
            else None

        # ROA
        # Total Assets
        if 'Total Assets' in yahoo_symbol_balancesheet.index:
            assets = yahoo_symbol_balancesheet.loc['Total Assets']
            if pd.isna(assets).all():
                assets = None
                assets_mean = None
                last_assets_mean = None
            else:
                assets = assets.dropna()
                assets_mean = (assets.shift(1) + assets) / 2
                last_assets_mean = assets_mean.dropna().iloc[0]
        else:
            assets = None
            assets_mean = None
            last_assets_mean = None

        roa = net_income_ttm / last_assets_mean \
            if net_income_ttm is not None \
            and last_assets_mean not in (None, 0) \
            else None

        # ------ Capital Efficiency ------ #
        # - wacc
        beta = yahoo_symbol_info.get("beta", None)

        cd = interest_expense_last / total_debt_last \
            if interest_expense_last is not None \
            and total_debt_last not in (None, 0) \
            else None

        # Tax Provision
        if 'Tax Provision' in yahoo_symbol_income_quarter.index:
            tax_provisory_quarter = yahoo_symbol_income_quarter.loc['Tax Provision']
            if pd.isna(tax_provisory_quarter).all():
                tax_provisory_quarter = None
                tax_provisory_ttm = None
            else:
                tax_provisory_quarter = tax_provisory_quarter.dropna()
                tax_provisory_ttm = tax_provisory_quarter.sum()
        else:
            tax_provisory_quarter = None
            tax_provisory_ttm = None

        # Pretax Income
        if 'Pretax Income' in yahoo_symbol_income_quarter.index:
            pretax_income_quarter = yahoo_symbol_income_quarter.loc['Pretax Income']
            if pd.isna(pretax_income_quarter).all():
                pretax_income_quarter = None
                pretax_income_ttm = None
            else:
                pretax_income_quarter = pretax_income_quarter.dropna()
                pretax_income_ttm = pretax_income_quarter.sum()
        else:
            pretax_income_quarter = None
            pretax_income_ttm = None

        tax_efective = tax_provisory_ttm / pretax_income_ttm \
            if tax_provisory_ttm is not None \
            and pretax_income_ttm not in (None, 0) \
            else None

        market_cap = yahoo_symbol_info.get('marketCap')

        us10y = yf.Ticker("^TNX").info.get("previousClose")
        us10y = us10y / 100 \
            if us10y is not None \
            else None

        erp = 0.055

        ce = us10y + beta * erp \
            if us10y is not None \
            and beta is not None \
            else None

        wacc = None
        if all(v is not None for v in [market_cap, total_debt_last, ce, cd, tax_efective]):
            total_cap = market_cap + total_debt_last
            if total_cap and total_cap > 0:
                wacc = ((market_cap / total_cap) * ce) + ((total_debt_last / total_cap) * cd * (1 - tax_efective))

        # WACCvsROIC
        eva = roic - wacc \
            if roic is not None \
            and wacc is not None \
            else None

        # ------ Growth ------ #
        # revenue growth
        growth_revenue_yoy = (total_revenue_fy.iloc[0] / total_revenue_fy.iloc[1]) - 1 \
            if isinstance(total_revenue_fy, pd.Series) and len(total_revenue_fy.dropna()) >= 2 else None

        cagr_growth_revenue_yoy = fm.get_cagr_metric(total_revenue_fy)
        if cagr_growth_revenue_yoy is not None and math.isnan(cagr_growth_revenue_yoy):
            cagr_growth_revenue_yoy = None

        # eps growth
        # Diluted EPS
        if 'Diluted EPS' in yahoo_symbol_income.index:
            dilutedEPS_fy = yahoo_symbol_income.loc['Diluted EPS']
            if pd.isna(dilutedEPS_fy).all():
                dilutedEPS_fy = None
            else:
                dilutedEPS_fy = dilutedEPS_fy.dropna()
        else:
            dilutedEPS_fy = None

        growth_eps_yoy = (dilutedEPS_fy.iloc[0] / dilutedEPS_fy.iloc[1]) - 1 \
            if isinstance(dilutedEPS_fy, pd.Series) and len(dilutedEPS_fy.dropna()) >= 2 else None

        cagr_growth_eps_yoy = fm.get_cagr_metric(dilutedEPS_fy)
        if cagr_growth_eps_yoy is not None and math.isnan(cagr_growth_eps_yoy):
            cagr_growth_eps_yoy = None

        # ------ Dividends ------ #
        # dividend yield
        dividendYield = yahoo_symbol_info.get("dividendYield", None)
        dividendYield = dividendYield / 100 \
            if dividendYield is not None \
            else None

        # payout ratio
        payout_ratio = yahoo_symbol_info.get("payoutRatio", None)

        # Dividend TTM
        s = yahoo_symbol_dividends if isinstance(yahoo_symbol_dividends, pd.Series) else pd.Series(dtype=float)
        s = s.sort_index()
        last_date = s.index[-1] if len(s) else None

        if len(s):
            annual = s.groupby(s.index.year).sum().sort_index()
            current_year = last_date.year
            annual_complete = annual.drop(index=current_year) if current_year in annual.index else annual.copy()
            cagr_dividend_3y = fm.get_cagr_metric(annual_complete.tail(3)) if len(annual_complete) >= 2 else None
            cagr_dividend_5y = fm.get_cagr_metric(annual_complete.tail(5)) if len(annual_complete) >= 2 else None
        else:
            cagr_dividend_3y = None
            cagr_dividend_5y = None

        # Shareholders Yield
        # cash dividend paid
        if 'Cash Dividends Paid' in yahoo_symbol_cashflow_quarter.index:
            cash_dividends_paid = yahoo_symbol_cashflow_quarter.loc['Cash Dividends Paid']
            if pd.isna(cash_dividends_paid).all():
                cash_dividends_paid = None
            else:
                cash_dividends_paid = cash_dividends_paid.dropna()
        else:
            cash_dividends_paid = None

        # rewards ttm
        if 'Repurchase Of Capital Stock' in yahoo_symbol_cashflow_quarter.index:
            rewards = yahoo_symbol_cashflow_quarter.loc['Repurchase Of Capital Stock']
            if pd.isna(rewards).all():
                rewards = None
            else:
                rewards = rewards.dropna()
        else:
            rewards = None

        div_ttm_quarter = cash_dividends_paid.sum() \
            if cash_dividends_paid is not None \
            else None
        rewards_ttm_quarter = rewards.sum() \
            if rewards is not None \
            else None

        shy = (div_ttm_quarter + rewards_ttm_quarter) / market_cap \
            if market_cap is not None \
            and div_ttm_quarter is not None \
            and rewards_ttm_quarter is not None \
            else None

        fiveYearAvgDY = yahoo_symbol_info.get("fiveYearAvgDividendYield", None)
        fiveYearAvgDividendYield = fiveYearAvgDY / 100 \
            if fiveYearAvgDY is not None \
            else None

        eps_ann = yahoo_symbol_info.get("epsCurrentYear", None)
        dividend_rate = yahoo_symbol_info.get("dividendRate", None)
        if (
            eps_ann is not None and
            dividend_rate is not None and
            dividend_rate != 0 and
            not math.isnan(eps_ann) and
            not math.isnan(dividend_rate)
        ):
            div_coverage_rate = eps_ann / dividend_rate
        else:
            div_coverage_rate = None

        # ------ Dividends ------ #
        # Beta
        sharesPercentSharesOut = yahoo_symbol_info.get("sharesPercentSharesOut", None)
        recommendationMean = yahoo_symbol_info.get("recommendationMean", None)
        targetMeanPrice = yahoo_symbol_info.get("targetMeanPrice", None)

        # ------ Extras ------ #
        yahoo_symbol_fundamental_info = {
            "kpis": {
                "trailingPE": trailing_pe,
                "forwardPE": forward_pe,
                "sectorTrailingPE": sector_pe,
                "PriceToSale": p_s,
                "evEbitda": ev_ebitda,
                "EquityFCFYield": fcf_yield_equity,
                "EnterpriseFCFYield": fcf_yield_enterp,
                "NetDebtEbitda": net_debt_ebitda,
                "InterestCoverageEbit": interest_coverage_ebit,
                "CurrentRatio": current_ratio,
                "QuickRatio": quick_ratio,
                "OperationalMargin": operation_margin,
                "FcfMargin": fcf_margin,
                "ROE": roe,
                "ROA": roa,
                "WACC": wacc,
                "ROIC": roic,
                "EVA": eva,
                "GrowthReveneuYoY": growth_revenue_yoy,
                "CagrGrowthReveneuYoY": cagr_growth_revenue_yoy,
                "GrowthEPSYoY": growth_eps_yoy,
                "CagrGrowthEPSYoY": cagr_growth_eps_yoy,
                "divCoverageRate": div_coverage_rate,
                "dividendYield": dividendYield,
                "PayoutRatio": payout_ratio,
                "CagrGrowthDividend3y": cagr_dividend_3y,
                "CagrGrowthDividend5y": cagr_dividend_5y,
                "ShareHolderYield": shy,
                "fiveYearAvgDividendYield": fiveYearAvgDividendYield,
            },
            "valuation": {
                "MarketCap": market_cap,
                "EVenterpriseValue": enterprise_value,
                "ebitdaTTM": ebitda_ttm,
            },
            "finantial_health": {
                "StockholdersEquity": stockholders_equity_last,
            },
            "profitability": {
                "NetIncome": net_income_ttm,
                "TotalRevenue": total_revenue_last,
            },
            "cashflow": {
                "FreeCashflow": free_cashflow_ttm,
            },
            "ratios": {
                # Margins
                "GrossMargin": 9999
            },
            "market_risk_and_sentiment": {
                "beta": beta,
                "sharesPercentSharesOut": sharesPercentSharesOut,
                "recommendationMean": recommendationMean,
                "targetMeanPrice": targetMeanPrice
            }
        }
        return yahoo_symbol_fundamental_info

    def get_symbol_inside_transactions(self, symbol: str):
        '''
        Return the list of inside transactions
        '''
        yahoo_symbol_insider_transactions = yf.Ticker(symbol).insider_transactions
        yahoo_symbol_insider_transactions = yahoo_symbol_insider_transactions.rename(columns={'Start Date': 'StartDate'})
        yahoo_symbol_insider_transactions.drop(columns=['URL', 'Transaction'], inplace=True)
        return yahoo_symbol_insider_transactions

    # ------------ FOREX ------------
    # ------- NOT IN USE ------

    def get_yahoo_symbol_calendar(self, symbol: str):
        '''
        Return corporative calendar events about asset
        '''
        yahoo_symbol_calendar = yf.Ticker(symbol).calendar
        return yahoo_symbol_calendar

    # ----------- Full Downloads -----------
    def get_yahoo_symbol_balance_sheet(self, symbol: str):
        '''
        Return the patrimonial balance sheet
        '''
        yahoo_symbol_balance_sheet = yf.Ticker(symbol).balance_sheet
        return yahoo_symbol_balance_sheet

    def get_yahoo_symbol_balance_sheet_quarterly(self, symbol: str):
        '''
        Return the patrimonial balance sheet in quarterly basis
        '''
        yahoo_symbol_balance_sheet_quarterly = yf.Ticker(symbol).quarterly_balance_sheet
        return yahoo_symbol_balance_sheet_quarterly

    def get_yahoo_symbol_cashflow(self, symbol: str):
        '''
        Return the cashflow results
        '''
        yahoo_symbol_cashflow = yf.Ticker(symbol).cashflow
        return yahoo_symbol_cashflow

    def get_yahoo_symbol_cashflow_quarterly(self, symbol: str):
        '''
        Return the cashflow results in a quarterly basis
        '''
        yahoo_symbol_cashflow_quarterly = yf.Ticker(symbol).quarterly_cashflow
        return yahoo_symbol_cashflow_quarterly

    def get_yahoo_symbol_income(self, symbol: str):
        '''
        Return the income statment
        '''
        yahoo_symbol_income = yf.Ticker(symbol).income_stmt
        return yahoo_symbol_income

    def get_yahoo_symbol_income_quarterly(self, symbol: str):
        '''
        Return the income statment in a quarterly basis
        '''
        yahoo_symbol_income_quarterly = yf.Ticker(symbol).quarterly_income_stmt
        return yahoo_symbol_income_quarterly

    def get_yahoo_symbol_financials(self, symbol: str):
        '''
        !!! Not Working !!!
        Return the financials results (profits and expenses)
        '''
        yahoo_symbol_financials = yf.Ticker(symbol).financials
        return yahoo_symbol_financials

    def get_yahoo_symbol_sustainability(self, symbol: str):
        '''
        Return the ESG metrics (enviormental, social and governamental)
        '''
        yahoo_symbol_sustainability = yf.Ticker(symbol).sustainability
        return yahoo_symbol_sustainability

    # ------------- News -------------
    def get_yahoo_symbol_news(self, symbol: str):
        '''
        Return the latest news about asset
        '''
        yahoo_symbol_news = yf.Ticker(symbol).news
        return yahoo_symbol_news

    # ------------- WORLD INDICES -------------
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

    # ----------- CRYPTOS -----------
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

    def get_yahoo_symbol_earnings_dates(self, symbol: str):
        '''
        Return the earnings of a symbol over time
        '''
        yahoo_data_earnings_dates = yf.Ticker(symbol).earnings_dates
        return yahoo_data_earnings_dates
