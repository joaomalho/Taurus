import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

class DataOpenInsider():

    def __init__(self, symbol: str, start_year: int = 2023, start_month: int = 1, max_workers: int = 5) -> None:
        
        self.symbol = symbol
        self.start_year = start_year
        self.start_month = start_month
        self.max_workers = max_workers

    def fetch_data(self, url: str) -> requests.Response:
        """
        Make an HTTP request to Open Insider to get the data.

        param :
            URL of transactions page from Open Insider.
        return : 
            Return the response of the request containing the HTML of the page.
            Generate an error if the response is bad (404, 500, etc.)
        """
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        return response


    def get_openinsider_data(self, year: int, month: int) -> pd.DataFrame:
        '''
        This method returns the data from openinsider.com
        '''
        
        start_date = datetime(year, month, 1).strftime('%m/%d/%Y')
        end_date = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        end_date = end_date.strftime('%m/%d/%Y')

        url = f"http://openinsider.com/screener?s={self.symbol}&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={start_date}+-+{end_date}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=5000&page=1"
        try:
            response = self.fetch_data(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'tinytable'})
            
            if not table:
                return pd.DataFrame()
            
            rows = table.find('tbody').findAll('tr')
            data = []

            for row in rows:
                cols = row.findAll('td')
                if not cols:
                    continue

                insider_data = {
                    "transaction_date": cols[0].text.strip(),
                    "trade_date": cols[1].text.strip(),
                    "ticker": self.symbol,
                    "company_name": cols[2].text.strip(),
                    "owner_name": cols[3].text.strip(),
                    "title": cols[4].text.strip(),
                    "transaction_type": cols[5].text.strip(),
                    "last_price": self.clean_numeric(cols[6].text),
                    "quantity": self.clean_numeric(cols[7].text),
                    "shares_held": self.clean_numeric(cols[8].text),
                    "owned_percentage": self.clean_numeric(cols[9].text),
                    "transaction_value": self.clean_numeric(cols[10].text)
                }

                data.append(insider_data)

            return pd.DataFrame(data)

        except Exception as e:
            return pd.DataFrame()

    def clean_numeric(self, value: str) -> float:
        """
        Converte numeric text to float, romving symbols.

        :parameters
            value: String containing numbers with formats regaring $, %, etc.
        :return: 
            Numbers converted to float.
        """
        if not value or value.lower() in ['n/a', 'new']:
            return 0.0
        clean = value.replace('$', '').replace(',', '')
        if '%' in clean:
            return 0.0
        try:
            return float(clean)
        except ValueError:
            return 9999999999999 
