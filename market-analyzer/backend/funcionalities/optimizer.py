import talib
import itertools
import numpy as np
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed
from datetime import datetime, timedelta

class ParamsOptimization():
    """
    A class for optimizing technical indicators' parameters and evaluating strategy performance.
    """

    def __init__(self):
        
        self.crossover_params = pd.DataFrame(columns=['Ticker', 'EMA1', 'EMA2', 'EMA3', 'Sharpe', 'MaxDrawdown', 'Expectancy'])
        self.bbands_params = pd.DataFrame(columns=['Ticker', 'Period', 'Std', 'Sharpe', 'MaxDrawdown', 'Expectancy'])

    def optimize(self, asset_type: str, symbol: str, period: str, interval: str):
        """
        Run optimization for all strategies.
        """
        data = self.fetch_data(asset_type, symbol, period, interval)
        self.crossover_results = self.optimize_crossover(data, symbol)
        self.bbands_results = self.optimize_bbands(data, symbol)


    def fetch_data(self,asset_type: str, symbol : str, period : str, interval : str):
        """
        Simulate fetching market data for the given ticker. According to same periodicity and timeframe of subject bot setting
        """

        if asset_type == 'stock':
            from backend.datasources.yahoodata import DataHistory
            dh = DataHistory()
            data = dh.get_yahoo_data_history(symbol, period, interval, start=datetime.now() - timedelta(days=365), end=datetime.now())

        elif asset_type == 'cambial':
            pass
            # Metatrader
        elif asset_type == 'crypto':
            pass
            # crypto
        return data

    def optimize_crossover(self, data : pd.DataFrame, symbol : str):
        """
        Optimize EMA crossover strategy.
        """
        ema1_periods = range(10, 21)
        ema2_periods = range(25, 61)
        ema3_periods = range(100, 200)

        combinations = list(itertools.product(ema1_periods, ema2_periods, ema3_periods))

        results = Parallel(n_jobs=-1)(delayed(self.simulate_crossover)(
            data, symbol, l1, l2, l3) for l1, l2, l3 in tqdm(combinations, desc="Optimizing EMA Crossover"))

        results_df = pd.DataFrame(results)

        return results_df

    def simulate_crossover(self, data : pd.DataFrame, symbol : str, l1 : int, l2 : int, l3 : int):
        """
        Simulate crossover strategy and calculate metrics.
        """
        # Calculate EMAs
        data['ema1'] = talib.EMA(data['Close'], timeperiod=l1)
        data['ema2'] = talib.EMA(data['Close'], timeperiod=l2)
        data['ema3'] = talib.EMA(data['Close'], timeperiod=l3)

        # Generate signals
        data['signal'] = np.where((data['ema1'] > data['ema2']) & (data['ema2'] > data['ema3']), 1,
                                  np.where((data['ema1'] < data['ema2']) & (data['ema2'] < data['ema3']), -1, 0))
        data['returns'] = data['Close'].pct_change() * data['signal'].shift(1)

        # Calculate metrics
        sharpe = self.calculate_sharpe(data['returns'])
        max_drawdown = self.calculate_max_drawdown(data['returns'])
        expectancy = self.calculate_expectancy(data['returns'])

        return {
            'Ticker': symbol,
            'EMA1': l1,
            'EMA2': l2,
            'EMA3': l3,
            'Sharpe': sharpe,
            'MaxDrawdown': max_drawdown,
            'Expectancy': expectancy
        }

    def optimize_bbands(self, data : pd.DataFrame, symbol : str):
        """
        Optimize Bollinger Bands strategy.
        """
        sma_periods = range(10, 21)
        std_devs = range(1, 3)

        combinations = list(itertools.product(sma_periods, std_devs))

        results = Parallel(n_jobs=-1)(delayed(self.simulate_bbands)(
            data, symbol, period, std) for period, std in tqdm(combinations, desc="Optimizing Bollinger Bands"))

        results_df = pd.DataFrame(results)
       
        return results_df

    def simulate_bbands(self, data, symbol, period, std):
        """
        Simulate Bollinger Bands strategy and calculate metrics.
        """
        # Calculate Bollinger Bands
        upperband, middleband, lowerband = talib.BBANDS(
            data['Close'], timeperiod=period, nbdevup=std, nbdevdn=std, matype=0
        )

        # Generate signals
        data['signal'] = np.where(data['Close'] < lowerband, 1,
                                  np.where(data['Close'] > upperband, -1, 0))
        data['returns'] = data['Close'].pct_change() * data['signal'].shift(1)

        # Calculate metrics
        sharpe = self.calculate_sharpe(data['returns'])
        max_drawdown = self.calculate_max_drawdown(data['returns'])
        expectancy = self.calculate_expectancy(data['returns'])

        return {
            'Ticker': symbol,
            'Period': period,
            'Std': std,
            'Sharpe': sharpe,
            'MaxDrawdown': max_drawdown,
            'Expectancy': expectancy
        }

    @staticmethod
    def calculate_sharpe(returns, risk_free_rate=0.025):
        """
        Calculate Sharpe Ratio.
        """
        mean_return = returns.mean()
        std_dev = returns.std()
        if std_dev == 0:
            return 0
        return (mean_return - risk_free_rate) / std_dev

    @staticmethod
    def calculate_max_drawdown(returns):
        """
        Calculate Max Drawdown.
        """
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = running_max - cumulative
        return drawdown.max()

    @staticmethod
    def calculate_expectancy(returns):
        """
        Calculate Expectancy.
        """
        wins = returns[returns > 0]
        losses = returns[returns < 0]
        win_rate = len(wins) / len(returns) if len(returns) > 0 else 0
        loss_rate = 1 - win_rate
        avg_win = wins.mean() if len(wins) > 0 else 0
        avg_loss = losses.mean() if len(losses) > 0 else 0
        return (win_rate * avg_win) - (loss_rate * avg_loss)

# Adicionar Fontes Crypt e Cambial
# Adicionar resultados