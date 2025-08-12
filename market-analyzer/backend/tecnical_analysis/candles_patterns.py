import talib
import numpy as np
from datetime import datetime, timedelta
from backend.risk_manager.risk_manager import RiskManagerTechnical


class CandlesPatterns:
    """
    Detect all candlestick patterns using TA-Lib.
    """

    def __init__(self):
        self

    def detect_pattern(self, data, pattern_function, pattern_name: str, dates):
        """
        General method to detect a specific candlestick pattern.
        """

        detection = pattern_function(data['Open'], data['High'], data['Low'], data['Close'])
        detected_indices = np.nonzero(detection)[0]

        results = []
        three_months_ago = datetime.now() - timedelta(days=90)

        for i in detected_indices:
            date = dates[i]

            if datetime.strptime(date, "%Y-%m-%d %H:%M") < three_months_ago:
                continue

            signal = int(detection[i])

            if pattern_name in [
                "doji", "dragonfly_doji", "gravestone_doji", "engulfing",
                "morning_star", "evening_star", "marubozu", "harami",
                "harami_cross", "kicking", "kicking_by_length", "tasuki_gap",
                "gap_side_by_side_white", "counter_attack", "piercing",
                "dark_cloud_cover", "tri_star", "spinning_top"
            ]:
                stoploss = round(data['Low'][i], 5) if signal > 0 else round(data['High'][i], 5)
            elif pattern_name in [
                "morning_doji_star", "hammer", "inverted_hammer",
                "thrusting", "matching_low", "three_white_soldiers",
                "three_outside", "three_stars_in_south"
            ]:
                stoploss = round(data['Low'][i], 5)
            elif pattern_name in [
                "evening_doji_star", "hanging_man", "shooting_star",
                "on_neck", "in_neck", "three_black_crows",
                "three_inside", "advance_block", "stalled_pattern"
            ]:
                stoploss = round(data['High'][i], 5)
            else:
                stoploss = None

            rmt = RiskManagerTechnical()
            # Utiliza a nova função para verificar se o Stoploss foi atingido
            future_close_prices = data['Close'][i + 1:i + 6]
            hit_stoploss = rmt.stoploss_candles_conditions(signal, stoploss, future_close_prices)

            if stoploss:
                results.append({
                    'Signal': signal,
                    'Stoploss': stoploss,
                    'Date': date,
                    'Result': hit_stoploss
                })

        return results

    def doji(self, data, dates): return self.detect_pattern(data, talib.CDLDOJI, "doji", dates)
    def dragonfly_doji(self, data, dates): return self.detect_pattern(data, talib.CDLDRAGONFLYDOJI, "dragonfly_doji", dates)
    def gravestone_doji(self, data, dates): return self.detect_pattern(data, talib.CDLGRAVESTONEDOJI, "gravestone_doji", dates)
    def engulfing(self, data, dates): return self.detect_pattern(data, talib.CDLENGULFING, "engulfing", dates)
    def morning_star(self, data, dates): return self.detect_pattern(data, talib.CDLMORNINGSTAR, "morning_star", dates)
    def evening_star(self, data, dates): return self.detect_pattern(data, talib.CDLEVENINGSTAR, "evening_star", dates)
    def morning_doji_star(self, data, dates): return self.detect_pattern(data, talib.CDLMORNINGDOJISTAR, "morning_doji_star", dates)
    def evening_doji_star(self, data, dates): return self.detect_pattern(data, talib.CDLEVENINGDOJISTAR, "evening_doji_star", dates)
    def hammer(self, data, dates): return self.detect_pattern(data, talib.CDLHAMMER, "hammer", dates)
    def inverted_hammer(self, data, dates): return self.detect_pattern(data, talib.CDLINVERTEDHAMMER, "inverted_hammer", dates)
    def hanging_man(self, data, dates): return self.detect_pattern(data, talib.CDLHANGINGMAN, "hanging_man", dates)
    def shooting_star(self, data, dates): return self.detect_pattern(data, talib.CDLSHOOTINGSTAR, "shooting_star", dates)
    def marubozu(self, data, dates): return self.detect_pattern(data, talib.CDLMARUBOZU, "marubozu", dates)
    def harami(self, data, dates): return self.detect_pattern(data, talib.CDLHARAMI, "harami", dates)
    def harami_cross(self, data, dates): return self.detect_pattern(data, talib.CDLHARAMICROSS, "harami_cross", dates)
    def spinning_top(self, data, dates): return self.detect_pattern(data, talib.CDLSPINNINGTOP, "spinning_top", dates)
    def kicking(self, data, dates): return self.detect_pattern(data, talib.CDLKICKING, "kicking", dates)
    def kicking_by_length(self, data, dates): return self.detect_pattern(data, talib.CDLKICKINGBYLENGTH, "kicking_by_length", dates)
    def tasuki_gap(self, data, dates): return self.detect_pattern(data, talib.CDLTASUKIGAP, "tasuki_gap", dates)
    def gap_side_by_side_white(self, data, dates): return self.detect_pattern(data, talib.CDLGAPSIDESIDEWHITE, "gap_side_by_side_white", dates)
    def counter_attack(self, data, dates): return self.detect_pattern(data, talib.CDLCOUNTERATTACK, "counter_attack", dates)
    def piercing(self, data, dates): return self.detect_pattern(data, talib.CDLPIERCING, "piercing", dates)
    def dark_cloud_cover(self, data, dates): return self.detect_pattern(data, talib.CDLDARKCLOUDCOVER, "dark_cloud_cover", dates)
    def tri_star(self, data, dates): return self.detect_pattern(data, talib.CDLTRISTAR, "tri_star", dates)
    def on_neck(self, data, dates): return self.detect_pattern(data, talib.CDLONNECK, "on_neck", dates)
    def in_neck(self, data, dates): return self.detect_pattern(data, talib.CDLINNECK, "in_neck", dates)
    def thrusting(self, data, dates): return self.detect_pattern(data, talib.CDLTHRUSTING, "thrusting", dates)
    def matching_low(self, data, dates): return self.detect_pattern(data, talib.CDLMATCHINGLOW, "matching_low", dates)
    def three_black_crows(self, data, dates): return self.detect_pattern(data, talib.CDL3BLACKCROWS, "three_black_crows", dates)
    def three_white_soldiers(self, data, dates): return self.detect_pattern(data, talib.CDL3WHITESOLDIERS, "three_white_soldiers", dates)
    def three_inside(self, data, dates): return self.detect_pattern(data, talib.CDL3INSIDE, "three_inside", dates)
    def three_outside(self, data, dates): return self.detect_pattern(data, talib.CDL3OUTSIDE, "three_outside", dates)
    def three_stars_in_south(self, data, dates): return self.detect_pattern(data, talib.CDL3STARSINSOUTH, "three_stars_in_south", dates)
    def advance_block(self, data, dates): return self.detect_pattern(data, talib.CDLADVANCEBLOCK, "advance_block", dates)
    def stalled_pattern(self, data, dates): return self.detect_pattern(data, talib.CDLSTALLEDPATTERN, "stalled_pattern", dates)

    # def abandoned_baby(self, data: pd.DataFrame):
    #     return self.detect_pattern(data, talib.CDLABANDONEDBABY, "abandoned_baby")

    # def unique_3_river(self, data: pd.DataFrame):
    #     return self.detect_pattern(data, talib.CDLUNIQUE3RIVER, "unique_3_river")

    # def belt_hold(self, data: pd.DataFrame):
    #     return self.detect_pattern(data, talib.CDLBELTHOLD, "belt_hold")

    # def separating_lines(self, data: pd.DataFrame):
    #     return self.detect_pattern(data, talib.CDLSEPARATINGLINES, "Separating Lines")

    # def upside_gap_two_crows(self, data: pd.DataFrame):
    #     return self.detect_pattern(data, talib.CDLUPSIDEGAP2CROWS, "Upside Gap Two Crows")
