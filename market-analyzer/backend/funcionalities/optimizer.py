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
        self.symbol = None
        self.market_type = None
        self.timeframe = None
        self.crossover_params = None
        self.bbands_params = None

    def fetch_data(self,asset_type: str, symbol : str, period : str, interval : str):
        """
        Simulate fetching market data for the given ticker. According to same periodicity and timeframe of subject bot setting
        """

        if asset_type == 'stock':
            from backend.datasources.yahoodata import DataHistory
            dh = DataHistory()
            data = dh.get_yahoo_data_history(symbol, period, interval, start=datetime.now(), end=datetime.now() - timedelta(days=365))

        elif asset_type == 'cambial':
            pass
            # Metatrader
        elif asset_type == 'crypto':
            pass
            # crypto
        
        return data

    def optimize(self, symbol : str):
        """
        Run optimization for all strategies.
        """
        data = self.fetch_data(symbol)
        self.crossover_params = self.optimize_crossover(data, symbol)
        self.bbands_params = self.optimize_bbands(data, symbol)
        
        
        return self.best_params

    def optimize_crossover(self, data : pd.DataFrame, symbol : str):
        """
        Optimize EMA crossover strategy.
        """
        ema1_periods = [10, 15, 20]
        ema2_periods = [25, 30, 50]
        ema3_periods = [100, 150, 200]

        combinations = list(itertools.product(ema1_periods, ema2_periods, ema3_periods))

        # Parallel execution for speed
        results = Parallel(n_jobs=-1)(delayed(self.simulate_crossover)(
            data, symbol, l1, l2, l3) for l1, l2, l3 in tqdm(combinations, desc="Optimizing EMA Crossover"))

        # Combine results into a DataFrame
        results_df = pd.DataFrame(results)
        best_result = results_df.loc[results_df['Expectancy'].idxmax()]

        return best_result

    def simulate_crossover(self, data : pd.DataFrame, symbol : str, l1 : int, l2 : int, l3 : int):
        """
        Simulate crossover strategy and calculate metrics.
        """
        # Calculate EMAs
        data['ema1'] = talib.EMA(data['close'], timeperiod=l1)
        data['ema2'] = talib.EMA(data['close'], timeperiod=l2)
        data['ema3'] = talib.EMA(data['close'], timeperiod=l3)

        # Generate signals
        data['signal'] = np.where((data['ema1'] > data['ema2']) & (data['ema2'] > data['ema3']), 1,
                                  np.where((data['ema1'] < data['ema2']) & (data['ema2'] < data['ema3']), -1, 0))
        data['returns'] = data['close'].pct_change() * data['signal'].shift(1)

        # Calculate metrics
        sharpe = self.calculate_sharpe(data['returns'])
        max_drawdown = self.calculate_max_drawdown(data['returns'])
        expectancy = self.calculate_expectancy(data['returns'])

        return {
            'Ticker': symbol,
            'Best_EMA1': l1,
            'Best_EMA2': l2,
            'Best_EMA3': l3,
            'Sharpe': sharpe,
            'Max_Drawdown': max_drawdown,
            'Expectancy': expectancy
        }

    def optimize_bbands(self, data : pd.DataFrame, symbol : str):
        """
        Optimize Bollinger Bands strategy.
        """
        sma_periods = [10, 15, 20]
        std_devs = [1, 2, 3]

        combinations = list(itertools.product(sma_periods, std_devs))

        # Parallel execution for speed
        results = Parallel(n_jobs=-1)(delayed(self.simulate_bbands)(
            data, symbol, period, std) for period, std in tqdm(combinations, desc="Optimizing Bollinger Bands"))

        # Combine results into a DataFrame
        results_df = pd.DataFrame(results)
        best_result = results_df.loc[results_df['Expectancy'].idxmax()]

        return best_result

    def simulate_bbands(self, data, symbol, period, std):
        """
        Simulate Bollinger Bands strategy and calculate metrics.
        """
        # Calculate Bollinger Bands
        upperband, middleband, lowerband = talib.BBANDS(
            data['close'], timeperiod=period, nbdevup=std, nbdevdn=std, matype=0
        )

        # Generate signals
        data['signal'] = np.where(data['close'] < lowerband, 1,
                                  np.where(data['close'] > upperband, -1, 0))
        data['returns'] = data['close'].pct_change() * data['signal'].shift(1)

        # Calculate metrics
        sharpe = self.calculate_sharpe(data['returns'])
        max_drawdown = self.calculate_max_drawdown(data['returns'])
        expectancy = self.calculate_expectancy(data['returns'])

        return {
            'Ticker': symbol,
            'Best_Period': period,
            'Best_Std': std,
            'Sharpe': sharpe,
            'Max_Drawdown': max_drawdown,
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