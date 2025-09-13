import math
import warnings
import requests
import numpy as np
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
        try:
            yahoo_symbol_cashflow = yf.Ticker(symbol).cash_flow
        except Exception:
            yahoo_symbol_cashflow = pd.DataFrame()
        try:
            yahoo_symbol_cashflow_quarter = yf.Ticker(symbol).quarterly_cash_flow
        except Exception:
            yahoo_symbol_cashflow_quarter = pd.DataFrame()
        try:
            yahoo_symbol_dividends = yf.Ticker(symbol).dividends
        except Exception:
            yahoo_symbol_dividends = pd.DataFrame()

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
        total_debt = yahoo_symbol_balancesheet.loc["Total Debt"].dropna().iloc[0]
        if total_debt is None or (isinstance(total_debt, float) and math.isnan(total_debt)):
            total_debt = None

        # - Minority Interest
        total_equity_gross_minority_interest = yahoo_symbol_balancesheet.loc["Total Equity Gross Minority Interest"].dropna().iloc[0]
        if total_equity_gross_minority_interest is None or (isinstance(total_equity_gross_minority_interest, float) and math.isnan(total_equity_gross_minority_interest)):
            total_equity_gross_minority_interest = None

        # - Stockholders Equity
        stockholders_equity = yahoo_symbol_balancesheet.loc["Stockholders Equity"].dropna().iloc[0]
        if stockholders_equity is None or (isinstance(stockholders_equity, float) and math.isnan(stockholders_equity)):
            stockholders_equity = None

        minority_interest = total_equity_gross_minority_interest - stockholders_equity

        preferred_equity = 0  # incluir se tiver a rubrica

        # - Debt & cash (preferidos)
        cash_sti = yahoo_symbol_balancesheet.loc["Cash Cash Equivalents And Short Term Investments"].dropna().iloc[0]
        if cash_sti is None:
            cash = yahoo_symbol_balancesheet.loc["Cash And Cash Equivalents"].dropna().iloc[0]
            sti = yahoo_symbol_balancesheet.loc["Other Short Term Investments"].dropna().iloc[0]
            cash_sti = (cash or 0) + (sti or 0)

        # - Enterprise Value
        enterprise_value = market_cap + total_debt + minority_interest + preferred_equity - cash_sti

        # - EBITDA
        ebitda_ttm = yahoo_symbol_income_quarter.loc["EBITDA"].sum()

        # - Total Revenue
        if 'Total Revenue' in yahoo_symbol_income_quarter.index:
            total_revenue = yahoo_symbol_income_quarter.loc['Total Revenue']
            if pd.isna(total_revenue).all():
                total_revenue = None
            else:
                total_revenue.dropna()

        # - Total Revenue FY
        if 'Total Revenue' in yahoo_symbol_income.index:
            total_revenue_fy = yahoo_symbol_income.loc['Total Revenue']
            if pd.isna(total_revenue_fy).all():
                total_revenue_fy = None
            else:
                total_revenue_fy = total_revenue_fy.dropna()

        total_revenue_ttm = total_revenue.sum()

        # - Free Cashflow
        if 'Free Cash Flow' in yahoo_symbol_cashflow_quarter.index:
            free_cashflow = yahoo_symbol_cashflow_quarter.loc['Free Cash Flow']
            if pd.isna(free_cashflow).all():
                free_cashflow = None

        free_cashflow_ttm = free_cashflow.sum()

        # - Métricas
        ev_ebitda = enterprise_value / ebitda_ttm if enterprise_value is not None and ebitda_ttm and ebitda_ttm > 0 else None
        p_s = market_cap / total_revenue_ttm if market_cap is not None and total_revenue_ttm and total_revenue_ttm > 0 else None
        fcf_yield_equity = free_cashflow_ttm / market_cap if free_cashflow_ttm is not None and market_cap and market_cap > 0 else None
        fcf_yield_enterp = free_cashflow_ttm / enterprise_value if free_cashflow_ttm is not None and enterprise_value and enterprise_value > 0 else None

        # ------ Finantial Health ------ #
        # - Net Debt / EBITDA
        net_debt = total_debt - cash_sti

        net_debt_ebitda = net_debt / ebitda_ttm if net_debt is not None and ebitda_ttm and ebitda_ttm > 0 else None

        # - Interest Coverage (EBIT)
        ebit_ttm = yahoo_symbol_income_quarter.loc["EBIT"].sum()

        interest_expense_ttm = yahoo_symbol_income.loc["Interest Expense"].dropna().iloc[0]  # sum(yahoo_symbol_income_quarter.loc["Interest Expense"])

        interest_expense_ttm = interest_expense_ttm if interest_expense_ttm is not None else None

        interest_coverage_ebit = ebit_ttm / interest_expense_ttm if ebit_ttm is not None and interest_expense_ttm and interest_expense_ttm > 0 else None

        # - Current Racio
        # current_assets
        if 'Current Assets' in yahoo_symbol_balancesheet_quarter.index:
            current_assets = yahoo_symbol_balancesheet_quarter.loc['Current Assets']
            if pd.isna(current_assets).all():
                current_assets = None
            else:
                current_assets = current_assets.dropna().iloc[0]
        # current_liabilities
        if 'Current Liabilities' in yahoo_symbol_balancesheet_quarter.index:
            current_liabilities = yahoo_symbol_balancesheet_quarter.loc['Current Liabilities']
            if pd.isna(current_liabilities).all():
                current_liabilities = None
            else:
                current_liabilities = current_liabilities.dropna().iloc[0]

        current_ratio = (current_assets / current_liabilities) if current_liabilities is not None else None

        # - Quick Racio
        # inventory
        if 'Inventory' in yahoo_symbol_balancesheet_quarter.index:
            inventory = yahoo_symbol_balancesheet_quarter.loc['Inventory']
            if pd.isna(inventory).all():
                inventory = None
            else:
                inventory = inventory.dropna().iloc[0]

        quick_ratio = ((current_assets - inventory) / current_liabilities)

        # ------ Profitability ------ #
        # operation_margin
        operation_margin = ebit_ttm / total_revenue_ttm if total_revenue_ttm is not None and total_revenue_ttm > 0 else None

        # fcf_margin
        fcf_margin = free_cashflow_ttm / total_revenue_ttm if total_revenue_ttm is not None and total_revenue_ttm > 0 else None

        # operating_income
        if 'Operating Income' in yahoo_symbol_income_quarter.index:
            operating_income = yahoo_symbol_income_quarter.loc['Operating Income']
            if pd.isna(operating_income).all():
                operating_income = None
            else:
                operating_income = operating_income.dropna().iloc[0]

        # ROIC
        tax_rate_ttm = yahoo_symbol_income_quarter.loc['Tax Rate For Calcs'].mean()
        cap_invested = yahoo_symbol_balancesheet.loc['Invested Capital']
        cap_invested_mean = (cap_invested.shift(1) + cap_invested) / 2
        last_capital = cap_invested_mean.dropna().iloc[0]
        nopat_ttm = (ebit_ttm * (1 - tax_rate_ttm))
        roic = nopat_ttm / last_capital if last_capital is not None else None

        # ROE
        # net_income_fy
        if 'Net Income' in yahoo_symbol_income.index:
            net_income_fy = yahoo_symbol_income.loc['Net Income']
            if pd.isna(net_income_fy).all():
                net_income_fy = None
            else:
                net_income_fy = net_income_fy.dropna()

        # net_income
        if 'Net Income' in yahoo_symbol_income_quarter.index:
            net_income = yahoo_symbol_income_quarter.loc['Net Income']
            if pd.isna(net_income).all():
                net_income = None
            else:
                net_income = net_income.dropna().iloc[0]

        net_income_ttm = net_income.sum()
        equity = yahoo_symbol_balancesheet.loc['Stockholders Equity']
        equity_mean = (equity.shift(1) + equity) / 2
        last_equity_mean = equity_mean.dropna().iloc[0]
        roe = net_income_ttm / last_equity_mean

        # ROA
        assets = yahoo_symbol_balancesheet.loc['Total Assets']
        assets_mean = (assets.shift(1) + assets) / 2
        last_assets_mean = assets_mean.dropna().iloc[0]
        roa = net_income_ttm / last_assets_mean

        # ------ Capital Efficiency ------ #
        # - wacc
        beta = yahoo_symbol_info.get("beta")
        interest_expense_ttm = yahoo_symbol_income.loc["Interest Expense"].dropna().iloc[0]
        total_debt = yahoo_symbol_balancesheet.loc["Total Debt"].dropna().iloc[0]

        cd = interest_expense_ttm / total_debt

        tax_provisory_ttm = yahoo_symbol_income_quarter.loc['Tax Provision'].sum()
        pretax_income_ttm = yahoo_symbol_income_quarter.loc['Pretax Income'].sum()
        tax_efective = tax_provisory_ttm / pretax_income_ttm

        market_cap = yahoo_symbol_info.get('marketCap')

        us10y = yf.Ticker("^TNX").info.get("previousClose") / 100
        erp = 0.055

        ce = us10y + beta * erp

        wacc = ((market_cap / (market_cap + total_debt)) * ce) + ((total_debt / (total_debt + market_cap)) * cd * (1 - tax_efective))

        # WACCvsROIC
        eva = roic - wacc

        # ------ Growth ------ #
        # revenue growth
        growth_revenue_yoy = (total_revenue_fy.iloc[0] / total_revenue_fy.iloc[1]) - 1 if total_revenue_fy.iloc[1] is not None else None
        cagr_growth_revenue_yoy = fm.get_cagr_metric(total_revenue_fy)
        if cagr_growth_revenue_yoy is not None and math.isnan(cagr_growth_revenue_yoy):
            cagr_growth_revenue_yoy = None

        # eps growth
        dilutedEPS_fy = yahoo_symbol_income.loc["Diluted EPS"].dropna()
        growth_eps_yoy = (dilutedEPS_fy.iloc[0] / dilutedEPS_fy.iloc[1]) - 1 if dilutedEPS_fy.iloc[1] is not None else None
        cagr_growth_eps_yoy = fm.get_cagr_metric(dilutedEPS_fy)
        if cagr_growth_eps_yoy is not None and math.isnan(cagr_growth_eps_yoy):
            cagr_growth_eps_yoy = None

        # ------ Dividends ------ #
        # dividend yield
        dividendYield = yahoo_symbol_info.get("trailingAnnualDividendYield", None),
        # payout ratio
        payout_ratio = yahoo_symbol_info.get("payoutRatio", None)

        # Dividend TTM
        s = yahoo_symbol_dividends.sort_index()
        last_date = s.index[-1]
        window_start = last_date - pd.Timedelta(days=365)
        div_ttm = float(s.loc[s.index > window_start].sum())

        # dividend growth
        annual = s.groupby(s.index.year).sum().sort_index()
        current_year = last_date.year
        # Se o último ano for o ano corrente, consideramos incompleto e removemos
        if current_year in annual.index:
            annual_complete = annual.drop(index=current_year)
        else:
            annual_complete = annual.copy()

        cagr_dividend_3y = fm.get_cagr_metric(annual_complete.tail(3))
        cagr_dividend_5y = fm.get_cagr_metric(annual_complete.tail(5))

        # Shareholders Yield
        # cash dividend paid
        if 'Cash Dividends Paid' in yahoo_symbol_cashflow_quarter.index:
            cash_dividends_paid = yahoo_symbol_cashflow_quarter.loc['Cash Dividends Paid']
            if pd.isna(cash_dividends_paid).all():
                cash_dividends_paid = None
            else:
                cash_dividends_paid = cash_dividends_paid.dropna()

        # rewards ttm
        if 'Repurchase Of Capital Stock' in yahoo_symbol_cashflow_quarter.index:
            rewards = yahoo_symbol_cashflow_quarter.loc['Repurchase Of Capital Stock']
            if pd.isna(rewards).all():
                rewards = None
            else:
                rewards = rewards.dropna()

        div_ttm_quarter = cash_dividends_paid.sum()
        rewards_ttm_quarter = rewards.sum()

        shy = (div_ttm_quarter + rewards_ttm_quarter) / market_cap if market_cap is not None else None

        fiveYearAvgDividendYield = yahoo_symbol_info.get("fiveYearAvgDividendYield", None)

        # ------ Extras ------ #
        eps_ann = yahoo_symbol_info.get("epsCurrentYear")
        dividend_rate = yahoo_symbol_info.get("dividendRate")
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

        # Profitability
        # cost_of_revenue
        if 'Cost Of Revenue' in yahoo_symbol_income.index:
            cost_of_revenue = yahoo_symbol_income.loc['Cost Of Revenue']
            if pd.isna(cost_of_revenue).all():
                cost_of_revenue = None

        # gross_profit
        if 'Gross Profit' in yahoo_symbol_income.index:
            gross_profit = yahoo_symbol_income.loc['Gross Profit']
            if pd.isna(gross_profit).all():
                gross_profit = None

        # operating_expenses
        if 'Operating Expense' in yahoo_symbol_income.index:
            operating_expenses = yahoo_symbol_income.loc['Operating Expense']
            if pd.isna(operating_expenses).all():
                operating_expenses = None

        cagr_cost_of_revenue = fm.get_cagr_metric(cost_of_revenue)
        if cagr_cost_of_revenue is not None and math.isnan(cagr_cost_of_revenue):
            cagr_cost_of_revenue = None
        cagr_total_revenue = fm.get_cagr_metric(total_revenue)
        if cagr_total_revenue is not None and math.isnan(cagr_total_revenue):
            cagr_total_revenue = None
        cagr_operating_expenses = fm.get_cagr_metric(operating_expenses)
        if cagr_operating_expenses is not None and math.isnan(cagr_operating_expenses):
            cagr_operating_expenses = None

        # Growth & NetWorth & Health
        # total_assets
        if 'Total Assets' in yahoo_symbol_balancesheet.index:
            total_assets = yahoo_symbol_balancesheet.loc['Total Assets']
            if pd.isna(total_assets).all():
                total_assets = None

        # current_liabilities
        if 'Current Liabilities' in yahoo_symbol_balancesheet.index:
            current_liabilities = yahoo_symbol_balancesheet.loc['Current Liabilities']
            if pd.isna(current_liabilities).all():
                current_liabilities = None

        # non_current_liabilities
        if 'Total Non Current Liabilities Net Minority Interest' in yahoo_symbol_balancesheet.index:
            non_current_liabilities = yahoo_symbol_balancesheet.loc['Total Non Current Liabilities Net Minority Interest']
            if pd.isna(non_current_liabilities).all():
                non_current_liabilities = None

        # total_liabilities
        if not current_liabilities.isna().all() and not non_current_liabilities.isna().all():
            total_liabilities = (current_liabilities + non_current_liabilities)
        else:
            total_liabilities = None

        # net_worth
        if not total_assets.isna().all() and not current_liabilities.isna().all() and not non_current_liabilities.isna().all():
            total_assets = total_assets.replace(0, np.nan)
            net_worth = total_assets.iloc[0] - total_liabilities.iloc[0]
        else:
            net_worth = None

        # current_assets
        if 'Current Assets' in yahoo_symbol_balancesheet.index:
            current_assets = yahoo_symbol_balancesheet.loc['Current Assets']
            if pd.isna(current_assets).all():
                current_assets = None

        # non_current_assets
        if 'Total Non Current Assets' in yahoo_symbol_balancesheet.index:
            non_current_assets = yahoo_symbol_balancesheet.loc['Total Non Current Assets']
            if pd.isna(non_current_assets).all():
                non_current_assets = None

        # short_term_debt_coverage
        if not current_assets.isna().all() and not current_liabilities.isna().all():
            short_term_debt_coverage = current_assets - current_liabilities
        else:
            short_term_debt_coverage = None

        # long_term_debt_coverage
        if not non_current_assets.isna().all() and not non_current_liabilities.isna().all():
            long_term_debt_coverage = non_current_assets - non_current_liabilities
        else:
            long_term_debt_coverage = None

        cagr_total_liabilities = fm.get_cagr_metric(total_liabilities)
        if cagr_total_liabilities is not None and math.isnan(cagr_total_liabilities):
            cagr_total_liabilities = None

        cagr_total_assets = fm.get_cagr_metric(total_assets)
        if cagr_total_assets is not None and math.isnan(cagr_total_assets):
            cagr_total_assets = None

        # cash_cash_equivalents
        if 'Cash And Cash Equivalents' in yahoo_symbol_balancesheet.index:
            cash_cash_equivalents = yahoo_symbol_balancesheet.loc['Cash And Cash Equivalents']
            if pd.isna(cash_cash_equivalents).all():
                cash_cash_equivalents = None

        # stockholders_equity
        if 'Stockholders Equity' in yahoo_symbol_balancesheet.index:
            stockholders_equity = yahoo_symbol_balancesheet.loc['Stockholders Equity']
            if pd.isna(stockholders_equity).all():
                stockholders_equity = None

        cagr_stockholder_equity = fm.get_cagr_metric(stockholders_equity)
        if cagr_stockholder_equity is not None and math.isnan(cagr_stockholder_equity):
            cagr_stockholder_equity = None

        # Cashflow
        # operating_cashflow
        if 'Operating Cash Flow' in yahoo_symbol_cashflow.index:
            operating_cashflow = yahoo_symbol_cashflow.loc['Operating Cash Flow']
            if pd.isna(operating_cashflow).all():
                operating_cashflow = None

        # capital_expenditure
        if 'Capital Expenditure' in yahoo_symbol_cashflow.index:
            capital_expenditure = yahoo_symbol_cashflow.loc['Capital Expenditure']
            if pd.isna(capital_expenditure).all():
                capital_expenditure = None

        # free_cashflow_yield
        if not pd.isna(market_cap) and market_cap != 0 and not free_cashflow.isna().all():
            free_cashflow_yield = (free_cashflow_ttm / market_cap)
        else:
            free_cashflow_yield = None

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
                "dividendTTM": div_ttm,
            },
            "valuation": {
                "MarketCap": market_cap,
                "EVenterpriseValue": enterprise_value,
                "ebitdaTTM": ebitda_ttm,
            },
            "finantial_health": {
                # Actual
                "TotalAssets": total_assets.iloc[0],
                "TotalLiabilities": total_liabilities.iloc[0],
                "NetWorth": net_worth,
                "CashCashEquivalents": cash_cash_equivalents.iloc[0],
                # Short Term 1y
                "ShortTermDebtCoverage": short_term_debt_coverage.iloc[0],
                "CurrentAssets": current_assets.iloc[0],
                "CurrentLiabilities": current_liabilities.iloc[0],
                # Long Term
                "LongTermDebtCoverage": long_term_debt_coverage.iloc[0],
                "NonCurrentAssets": non_current_assets.iloc[0],
                "NonCurrentLiabilities": non_current_liabilities.iloc[0],
                # Growth
                "TotalAssetsCAGR": cagr_total_assets,
                "TotalLiabilitiesCAGR": cagr_total_liabilities,
                # Stockholders Equity
                "StockholdersEquityCAGR": cagr_stockholder_equity,
                "StockholdersEquity": stockholders_equity.iloc[0],
            },
            "profitability": {
                "NetIncome": net_income_ttm,
                "TotalRevenue": total_revenue.iloc[0],
                "CostOfRevenue": cost_of_revenue.iloc[0],
                "GrossProfit": gross_profit.iloc[0],
                "OperatingExpenses": operating_expenses.iloc[0],
                "CostOfRevenueCAGR": cagr_cost_of_revenue,
                "TotalRevenueCAGR": cagr_total_revenue,
                "OperatingExpensesCAGR": cagr_operating_expenses,
            },
            "cashflow": {
                "FreeCashflow": free_cashflow_ttm,
                "OperatingCashflow": operating_cashflow.iloc[0],
                "CapitalExpenditure": capital_expenditure.iloc[0],
                "FreeCashflowYield": free_cashflow_yield,
            },
            "ratios": {
                # Margins
                "GrossMargin": 9999
            },
            "market_risk_and_sentiment": {
                "beta": yahoo_symbol_info.get("beta", None),
                "sharesPercentSharesOut": yahoo_symbol_info.get("sharesPercentSharesOut", None),
                "recommendationMean": yahoo_symbol_info.get("recommendationMean", None),
                "targetMeanPrice": yahoo_symbol_info.get("targetMeanPrice", None)
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
