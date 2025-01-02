import talib
import pandas as pd

class CandlesPatterns:
    """
    Detect all candlestick patterns using TA-Lib.
    """

    def __init__(self):
        self.result_candles_df = pd.DataFrame(columns=['Pattern', 'Signal', 'Relevance', 'Stoploss'])
        
        
    def detect_pattern(self, data: pd.DataFrame, pattern_function, pattern_name: str):
        """
        General method to detect a specific candlestick pattern.
        """
        data_pass = data  # Usar todos os candles fornecidos

        # Detect pattern
        detection = pattern_function(data_pass['Open'], data_pass['High'], data_pass['Low'], data_pass['Close'])

        # Localizar valores não-zero
        non_zero_detection = detection[detection != 0]
        if not non_zero_detection.empty:
            for date, signal in non_zero_detection.items():
                # Cálculo do Stoploss baseado no padrão
                if pattern_name in [
                    "doji", "dragonfly_doji", "gravestone_doji", "engulfing",
                    "morning_star", "evening_star", "marubozu", "harami",
                    "harami_cross", "kicking", "kicking_by_length", "tasuki_gap",
                    "gap_side_by_side_white", "counter_attack", "piercing",
                    "dark_cloud_cover", "tri_star"
                ]:
                    stoploss = data_pass.loc[date, 'Low'] if signal > 0 else data_pass.loc[date, 'High']
                elif pattern_name in [
                    "morning_doji_star", "hammer", "inverted_hammer",
                    "thrusting", "matching_low", "three_white_soldiers",
                    "three_outside", "three_stars_in_south"
                ]:
                    stoploss = data_pass.loc[date, 'Low']
                elif pattern_name in [
                    "evening_doji_star", "hanging_man", "shooting_star",
                    "on_neck", "in_neck", "three_black_crows",
                    "three_inside", "advance_block", "stalled_pattern"
                ]:
                    stoploss = data_pass.loc[date, 'High']
                else:
                    stoploss = None

                new_entry = pd.DataFrame({
                    'Pattern': [pattern_name],
                    'Signal': [signal],
                    'Relevance': ['Flat'],
                    'Stoploss': [stoploss],
                }, index=[date])
                self.result_candles_df = pd.concat([self.result_candles_df, new_entry], ignore_index=False)

        return detection

    def doji(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLDOJI, "doji")

    def dragonfly_doji(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLDRAGONFLYDOJI, "dragonfly_doji")

    def gravestone_doji(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLGRAVESTONEDOJI, "gravestone_doji")

    def engulfing(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLENGULFING, "engulfing")

    def morning_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLMORNINGSTAR, "morning_star")

    def evening_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLEVENINGSTAR, "evening_star")

    def morning_doji_star(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLMORNINGDOJISTAR, "morning_doji_star")

    def evening_doji_star(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLEVENINGDOJISTAR, "evening_doji_star")

    def hammer(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLHAMMER, "hammer")

    def inverted_hammer(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLINVERTEDHAMMER, "inverted_hammer")

    def hanging_man(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLHANGINGMAN, "hanging_man")

    def shooting_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLSHOOTINGSTAR, "shooting_star")

    def marubozu(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLMARUBOZU, "marubozu")

    def harami(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLHARAMI, "harami")

    def harami_cross(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLHARAMICROSS, "harami_cross")

    def spinning_top(self, data: pd.DataFrame):
        '''
        NEED FIBONACCI
        '''
        return self.detect_pattern(data, talib.CDLSPINNINGTOP, "spinning_top")

    def kicking(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLKICKING, "kicking")

    def kicking_by_length(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLKICKINGBYLENGTH, "kicking_by_length")

    def tasuki_gap(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLTASUKIGAP, "tasuki_gap")

    def gap_side_by_side_white(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLGAPSIDESIDEWHITE, "gap_side_by_side_white")

    def counter_attack(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLCOUNTERATTACK, "counter_attack")

    def piercing(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLPIERCING, "piercing")

    def dark_cloud_cover(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLDARKCLOUDCOVER, "dark_cloud_cover")

    def tri_star(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLTRISTAR, "tri_star")

    def on_neck(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLONNECK, "on_neck")

    def in_neck(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLINNECK, "in_neck")

    def thrusting(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLTHRUSTING, "thrusting")

    def matching_low(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLMATCHINGLOW, "matching_low")

    def three_black_crows(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDL3BLACKCROWS, "three_black_crows")

    def three_white_soldiers(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDL3WHITESOLDIERS, "three_white_soldiers")

    def three_inside(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDL3INSIDE, "three_inside")

    def three_outside(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDL3OUTSIDE, "three_outside")

    def three_stars_in_south(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDL3STARSINSOUTH, "three_stars_in_south")

    def advance_block(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLADVANCEBLOCK, "advance_block")

    def stalled_pattern(self, data: pd.DataFrame):
        # takeprofit = None
        return self.detect_pattern(data, talib.CDLSTALLEDPATTERN, "stalled_pattern")

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
