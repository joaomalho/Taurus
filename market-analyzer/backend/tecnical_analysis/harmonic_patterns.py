import numpy as np
from backend.funcionalities.formulas import Formulas


class HarmonicPatterns:
    """
    Detect all candlestick patterns using TA-Lib.
    """

    def __init__(self):
        self

    def get_gartley_hp(self, moves, err_allowed, stop_factor, price_X):
        XA, AB, BC, CD = moves

        AB_range = np.array([.618 - err_allowed, .618 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None,
            "STOP": None
        }

        # === Bullish Gartley === ##
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D + (price_C - price_D) * 1.618,
                    "STOP": price_D - abs(CD) * stop_factor
                })

                return 1, targets  # Bullish

        # === Bearish Gartley === ##
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D - (price_D - price_C) * 1.618,
                    "STOP": price_D + abs(CD) * stop_factor
                })

                return -1, targets  # Bearish

        return np.nan, targets

    def get_bat_hp(self, moves, err_allowed, stop_factor, price_X):
        XA, AB, BC, CD = moves

        AB_range = np.array([.382 - err_allowed, .5 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None,
            "STOP": None
        }

        # === Bullish Bat === ##
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D + (price_C - price_D) * 1.618,
                    "STOP": price_D - abs(CD) * stop_factor
                })

                return 1, targets  # Bullish

        # === Bearish Bat === ##
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D - (price_D - price_C) * 1.618,
                    "STOP": price_D + abs(CD) * stop_factor
                })

                return -1, targets  # Bearish

        return np.nan, targets

    def get_butterfly_hp(self, moves, err_allowed, stop_factor, price_X):
        XA, AB, BC, CD = moves

        AB_range = np.array([.786 - err_allowed, .786 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(XA)  # ou abs(BC)

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None,
            "STOP": None,
        }

        # === Bullish Butterfly === ##
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D + (price_C - price_D) * 1.618,
                    "STOP": price_D - abs(CD) * stop_factor
                })

                return 1, targets  # Bullish

        # === Bearish Butterfly === ##
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D - (price_D - price_C) * 1.618,
                    "STOP": price_D + abs(CD) * stop_factor
                })

                return -1, targets  # Bearish

        return np.nan, targets

    def get_crab_hp(self, moves, err_allowed, stop_factor, price_X):
        XA, AB, BC, CD = moves

        AB_range = np.array([.382 - err_allowed, .618 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([2.24 - err_allowed, 3.618 + err_allowed]) * abs(XA)

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None,
            "STOP": None,
        }

        # === Bullish Crab === ##
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D + (price_C - price_D) * 1.618,
                    "STOP": price_D - abs(CD) * stop_factor
                })

                return 1, targets  # Bullish

        # === Bearish Crab === ##
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
            if (AB_range[0] < abs(AB) < AB_range[1] and
                    BC_range[0] < abs(BC) < BC_range[1] and
                    CD_range[0] < abs(CD) < CD_range[1]):

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                price_D = price_X + D
                price_C = price_X + C
                price_B = price_X + B

                targets.update({
                    "XA": XA,
                    "AB": AB,
                    "BC": BC,
                    "CD": CD,
                    "TP1": price_B,
                    "TP2": price_C,
                    "TP3": price_D - (price_D - price_C) * 1.618,
                    "STOP": price_D + abs(CD) * stop_factor
                })

                return -1, targets  # Bearish

        return np.nan, targets

    def backtest_harmonic_patterns(self, data, err_allowed: float, order: int, stop_factor: float, future_window: int):
        close = data.Close.values
        results = []

        hp = HarmonicPatterns()
        fm = Formulas()

        for i in range(5, len(close) - future_window):
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
                "direction": int(direction),
                "hit_tp": hit_tp,
                "stop_hit": stop_hit,
                "D_index": int(D_index),
                "D_price": float(D_price),
                "CD_DIFF": float(targets.get("CD_DIFF")) if targets.get("CD_DIFF") is not None else None,
                "order": int(order),
                "err_allowed": float(err_allowed),
                "reward": float(reward) if reward is not None else None,
                "risk": float(risk) if risk is not None else None,
                "rr_ratio": float(rr_ratio) if rr_ratio is not None else None,
                "weighted_return": float(weighted_return) if weighted_return is not None else None,
                "STOP": float(stop_price) if stop_price is not None else None,
                "TP1": float(targets["TP1"]) if targets.get("TP1") is not None else None,
                "TP2": float(targets["TP2"]) if targets.get("TP2") is not None else None,
                "TP3": float(targets["TP3"]) if targets.get("TP3") is not None else None,
                "pattern_idx": [int(idx) for idx in current_idx],
                "pattern_idx_dates": data.Date.iloc[current_idx].astype(str).tolist(),
                "pattern_idx_prices": [float(p) for p in current_pat.tolist()]
            })

        return results
