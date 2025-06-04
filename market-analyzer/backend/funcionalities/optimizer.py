import talib
import itertools
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed

# NOVOS E IMPLEMENTADOS
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from backend.funcionalities.formulas import Formulas
from backend.tecnical_analysis.harmonic_patterns import HarmonicPatterns

class ParamsOptimization():
    """
    A class for optimizing technical indicators' parameters and evaluating strategy performance.
    """

    def __init__(self):
        self

    # NOVOS E FUNCIONAIS, PARA CIMA NÃO IMPLEMENTADO

    def backtest_harmonic_patterns(self, data, err_allowed=0.02, order=5, stop_factor=0.1, future_window=20):
        
        hp = HarmonicPatterns()
        fm = Formulas()

        close = data.Close.values
        results = []

        for i in tqdm(range(100, len(close) - future_window)):
            current_idx, current_pat, start, end, idx = fm.peak_detect(close[:i], order=order)
            if len(current_pat) < 5:
                continue

            XA = current_pat[1] - current_pat[0]
            AB = current_pat[2] - current_pat[1]
            BC = current_pat[3] - current_pat[2]
            CD = current_pat[4] - current_pat[3]
            moves = [XA, AB, BC, CD]
            price_X = current_pat[0]

            patterns = [
                hp.get_gartley_hp(moves, err_allowed, stop_factor, price_X),
                hp.get_butterfly_hp(moves, err_allowed, stop_factor, price_X),
                hp.get_bat_hp(moves, err_allowed, stop_factor, price_X),
                hp.get_crab_hp(moves, err_allowed, stop_factor, price_X)
            ]

            pattern_names = ['Gartley', 'Butterfly', 'Bat', 'Crab']

            valid_patterns = [
                (name, p[0], p[1])
                for name, p in zip(pattern_names, patterns)
                if isinstance(p, tuple) and not np.isnan(p[0])
            ]

            if not valid_patterns:
                continue

            best = min(valid_patterns, key=lambda x: x[2].get("CD_DIFF", float('inf')))
            name, direction, targets = best

            D_index = current_idx[-1]
            D_price = current_pat[-1]
            stop_price = targets.get("STOP")
            future_prices = close[D_index:D_index + future_window]

            hit_tp = None
            stop_hit = False

            for price in future_prices:
                if direction == 1 and price <= stop_price:
                    stop_hit = True
                    break
                elif direction == -1 and price >= stop_price:
                    stop_hit = True
                    break

                for tp_name in ['TP1', 'TP2', 'TP3']:
                    tp = targets[tp_name]
                    if tp is None:
                        continue

                    if (direction == 1 and price >= tp) or (direction == -1 and price <= tp):
                        hit_tp = tp_name
                        break
                if hit_tp:
                    break

            # ==== Reward/Risk ====
            reward = None
            risk = None
            rr_ratio = None
            weighted_return = None

            if hit_tp:
                reward = abs(targets[hit_tp] - D_price)
            if stop_price:
                risk = abs(stop_price - D_price)
            if reward and risk and risk > 0:
                rr_ratio = reward / risk

            if hit_tp:
                weighted_return = reward
            elif stop_hit:
                weighted_return = -risk

            results.append({
                "pattern": name,
                "direction": direction,
                "hit_tp": hit_tp,
                "stop_hit": stop_hit,
                "D_index": D_index,
                "D_price": D_price,
                "CD_DIFF": targets.get("CD_DIFF"),
                "order": order,
                "err_allowed": err_allowed,
                "reward": reward,
                "risk": risk,
                "rr_ratio": rr_ratio,
                "weighted_return": weighted_return
            })

        return results


    def simulate_trading(self, results, initial_capital, risk_per_trade):

        df = pd.DataFrame(results)
        df = df.dropna(subset=["risk"]) 

        capital = initial_capital
        equity_curve = []
        trades = []

        for idx, row in df.iterrows():
            risk_amount = capital * risk_per_trade

            if row['risk'] == 0 or pd.isna(row['risk']):
                continue  # evitar divisões por zero

            # Tamanho da posição baseado no risco
            position_size = risk_amount / row['risk']

            if row['hit_tp']:
                gain = position_size * row['reward']
                capital += gain
                trades.append({"result": "win", "pnl": gain})
            elif row['stop_hit']:
                loss = -risk_amount
                capital += loss
                trades.append({"result": "loss", "pnl": loss})
            else:
                # Nenhum TP ou stop atingido → neutro
                trades.append({"result": "neutral", "pnl": 0})

            equity_curve.append(capital)

        equity_df = pd.DataFrame(trades)
        equity_df['capital'] = equity_curve

        return equity_df


    def normalize_decision_rank(self, resumo):
        # Cópia de trabalho
        resumo_norm = resumo.copy()

        # Garantir que não há NaNs nas colunas-chave antes de normalizar
        cols_to_normalize = [
            "capital_final",
            "expectancy",
            "reward_risk_medio",
            "retorno_ponderado_medio",
            "lucro_por_trade"
        ]

        # Preencher NaNs com o mínimo (tratamento conservador)
        for col in cols_to_normalize:
            if col in resumo_norm.columns:
                min_val = resumo_norm[col].min()
                resumo_norm[col] = resumo_norm[col].fillna(min_val)

        # Normalizar (0 a 1)
        scaler = MinMaxScaler()
        normalized = pd.DataFrame(
            scaler.fit_transform(resumo_norm[cols_to_normalize]),
            columns=[col + "_norm" for col in cols_to_normalize]
        )

        # Juntar colunas normalizadas
        resumo_norm = pd.concat([resumo_norm.reset_index(drop=True), normalized], axis=1)

        # Score ponderado (ajuste pesos conforme a tua estratégia)
        resumo_norm["score"] = (
            resumo_norm["capital_final_norm"] * 0.40 +
            resumo_norm["expectancy_norm"] * 0.25 +
            resumo_norm["reward_risk_medio_norm"] * 0.15 +
            resumo_norm["retorno_ponderado_medio_norm"] * 0.15 +
            resumo_norm["lucro_por_trade_norm"] * 0.05
        )

        # Ranking
        resumo_norm = resumo_norm.sort_values(by="score", ascending=False)
        resumo_norm["ranking"] = range(1, len(resumo_norm) + 1)

        return resumo_norm

    def run_full_backtest(self, data, future_window=20):
        """
        Testa várias combinações de (order, err_allowed, stop_factor) e avalia performance dos padrões harmônicos.
        
        Return:
            summary_df: DataFrame com estatísticas de acerto e capital final por combinação
        """
        po = ParamsOptimization()
        summary = []

        # orders = [2, 3, 4, 5]
        # err_values = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
        # stop_factors = [0.1, 0.2]
        orders = [5]
        err_values = [0.05, 0.06]
        stop_factors = [0.1, 0.2]
        capex = 10000
        risk_per_trade=0.01

        summary = []

        for order in orders:
            for err in err_values:
                for stop in stop_factors:
                    
                    # Roda o backtest
                    results = po.backtest_harmonic_patterns(
                        data,
                        err_allowed=err,
                        order=order,
                        stop_factor=stop,
                        future_window=future_window
                    )
                    df = pd.DataFrame(results)

                    total = len(df)
                    hits = df['hit_tp'].notna().sum()
                    success_rate = hits / total if total > 0 else 0

                    # Estatísticas de retorno
                    rr_mean = df['rr_ratio'].mean()
                    reward_mean = df['reward'].mean()
                    risk_mean = df['risk'].mean()
                    weighted_return_mean = df['weighted_return'].mean()

                    # Simulação de capital
                    equity_df = po.simulate_trading(results, initial_capital=capex)
                    final_capital = equity_df['capital'].iloc[-1] if not equity_df.empty else None

                    taxa_acerto = round(success_rate * 100, 2)
                    reward_medio = round(reward_mean, 4) if reward_mean else None
                    risk_medio = round(risk_mean, 4) if risk_mean else None
                    reward_risk_medio = round(rr_mean, 4) if rr_mean else None
                    retorno_ponderado_medio = round(weighted_return_mean, 4) if weighted_return_mean else None
                    capital_final = round(final_capital, 2) if final_capital else None

                    expectancy = (
                        (taxa_acerto / 100) * reward_risk_medio - (1 - taxa_acerto / 100)
                    ) if reward_risk_medio is not None else None

                    lucro_por_trade = (
                        (capital_final - capex) / total if total > 0 else None
                    )

                    summary.append({
                        "order": order,
                        "err_allowed": err,
                        "stop_factor": stop,
                        "padroes_detectados": total,
                        "targets_atingidos": hits,
                        "taxa_acerto": taxa_acerto,
                        "reward_medio": reward_medio,
                        "risk_medio": risk_medio,
                        "reward_risk_medio": reward_risk_medio,
                        "retorno_ponderado_medio": retorno_ponderado_medio,
                        "expectancy": expectancy,
                        "lucro_por_trade": lucro_por_trade,
                        "capital_final": capital_final
                    })

        summary_df = pd.DataFrame(summary)
        summary_df = summary_df.sort_values(by="capital_final", ascending=False)

        po.normalize_decision_rank(summary_df)

        return summary_df
    

## POR IMPLEMENTAR

#     def optimize_crossover(self, data : pd.DataFrame, symbol : str):
#         """
#         Optimize EMA crossover strategy.
#         """
#         ema1_periods = range(10, 21)
#         ema2_periods = range(25, 61)
#         ema3_periods = range(100, 200)

#         combinations = list(itertools.product(ema1_periods, ema2_periods, ema3_periods))

#         results = Parallel(n_jobs=-1)(delayed(self.simulate_crossover)(
#             data, symbol, l1, l2, l3) for l1, l2, l3 in tqdm(combinations, desc="Optimizing EMA Crossover"))

#         results_df = pd.DataFrame(results)

#         return results_df

#     def simulate_crossover(self, data : pd.DataFrame, symbol : str, l1 : int, l2 : int, l3 : int):
#         """
#         Simulate crossover strategy and calculate metrics.
#         """
#         # Calculate EMAs
#         data['ema1'] = talib.EMA(data['Close'], timeperiod=l1)
#         data['ema2'] = talib.EMA(data['Close'], timeperiod=l2)
#         data['ema3'] = talib.EMA(data['Close'], timeperiod=l3)

#         # Generate signals
#         data['signal'] = np.where((data['ema1'] > data['ema2']) & (data['ema2'] > data['ema3']), 1,
#                                   np.where((data['ema1'] < data['ema2']) & (data['ema2'] < data['ema3']), -1, 0))
#         data['returns'] = data['Close'].pct_change() * data['signal'].shift(1)

#         # Calculate metrics
#         sharpe = self.calculate_sharpe(data['returns'])
#         max_drawdown = self.calculate_max_drawdown(data['returns'])
#         expectancy = self.calculate_expectancy(data['returns'])

#         return {
#             'Ticker': symbol,
#             'EMA1': l1,
#             'EMA2': l2,
#             'EMA3': l3,
#             'Sharpe': sharpe,
#             'MaxDrawdown': max_drawdown,
#             'Expectancy': expectancy
#         }

#     def optimize_bbands(self, data : pd.DataFrame, symbol : str):
#         """
#         Optimize Bollinger Bands strategy.
#         """
#         sma_periods = range(10, 21)
#         std_devs = range(1, 3)

#         combinations = list(itertools.product(sma_periods, std_devs))

#         results = Parallel(n_jobs=-1)(delayed(self.simulate_bbands)(
#             data, symbol, period, std) for period, std in tqdm(combinations, desc="Optimizing Bollinger Bands"))

#         results_df = pd.DataFrame(results)
       
#         return results_df

#     def simulate_bbands(self, data, symbol, period, std):
#         """
#         Simulate Bollinger Bands strategy and calculate metrics.
#         """
#         # Calculate Bollinger Bands
#         upperband, middleband, lowerband = talib.BBANDS(
#             data['Close'], timeperiod=period, nbdevup=std, nbdevdn=std, matype=0
#         )

#         # Generate signals
#         data['signal'] = np.where(data['Close'] < lowerband, 1,
#                                   np.where(data['Close'] > upperband, -1, 0))
#         data['returns'] = data['Close'].pct_change() * data['signal'].shift(1)

#         # Calculate metrics
#         sharpe = self.calculate_sharpe(data['returns'])
#         max_drawdown = self.calculate_max_drawdown(data['returns'])
#         expectancy = self.calculate_expectancy(data['returns'])

#         return {
#             'Ticker': symbol,
#             'Period': period,
#             'Std': std,
#             'Sharpe': sharpe,
#             'MaxDrawdown': max_drawdown,
#             'Expectancy': expectancy
#         }

#     @staticmethod
#     def calculate_sharpe(returns, risk_free_rate=0.025):
#         """
#         Calculate Sharpe Ratio.
#         """
#         mean_return = returns.mean()
#         std_dev = returns.std()
#         if std_dev == 0:
#             return 0
#         return (mean_return - risk_free_rate) / std_dev

#     @staticmethod
#     def calculate_max_drawdown(returns):
#         """
#         Calculate Max Drawdown.
#         """
#         cumulative = (1 + returns).cumprod()
#         running_max = cumulative.cummax()
#         drawdown = running_max - cumulative
#         return drawdown.max()

#     @staticmethod
#     def calculate_expectancy(returns):
#         """
#         Calculate Expectancy.
#         """
#         wins = returns[returns > 0]
#         losses = returns[returns < 0]
#         win_rate = len(wins) / len(returns) if len(returns) > 0 else 0
#         loss_rate = 1 - win_rate
#         avg_win = wins.mean() if len(wins) > 0 else 0
#         avg_loss = losses.mean() if len(losses) > 0 else 0
#         return (win_rate * avg_win) - (loss_rate * avg_loss)

# # Adicionar Fontes Crypt e Cambial
# # Adicionar resultados