import requests
import warnings
from decimal import Decimal
from datetime import datetime

warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")

class DataHistoryCrypto():

    def __init__(self) -> None:
        self

    def get_crypto_symbol_price(self, symbol : str):

        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": symbol}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            price = response.json()["price"]
        else:
            error = print(f"Erro: {response.status_code} - {response.text}")

        return symbol, price, error

    def get_crypto_symbol_24h(self, symbol : str):

        url = "https://api.binance.com/api/v3/ticker/24hr"
        params = {"symbol": symbol}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            self.priceChangePercent = Decimal(response.json()["priceChangePercent"])
            self.weightedAvgPrice = Decimal(response.json()["weightedAvgPrice"])
            self.prevClosePrice = Decimal(response.json()["prevClosePrice"])
            self.priceChange = Decimal(response.json()["priceChange"])
            self.lastPrice = Decimal(response.json()["lastPrice"])
            self.lastQty = Decimal(response.json()["lastQty"])
            self.bidPrice = Decimal(response.json()["bidPrice"])
            self.bidQty = Decimal(response.json()["bidQty"])
            self.askPrice = Decimal(response.json()["askPrice"])
            self.askQty = Decimal(response.json()["askQty"])
            self.openPrice = Decimal(response.json()["openPrice"])
            self.highPrice = Decimal(response.json()["highPrice"])
            self.lowPrice = Decimal(response.json()["lowPrice"])
            self.volume = Decimal(response.json()["volume"])
            self.quoteVolume = Decimal(response.json()["quoteVolume"])
            self.openTime = datetime.fromtimestamp(response.json()["openTime"] / 1000).strftime("%d-%m-%Y %H:%M:%S")
            self.closeTime = datetime.fromtimestamp(response.json()["closeTime"] / 1000).strftime("%d-%m-%Y %H:%M:%S")
            self.firstId = response.json()["firstId"]
            self.lastId = response.json()["lastId"]
            self.count = response.json()["count"]
        else:
            print(f"Erro: {response.status_code} - {response.text}")

    