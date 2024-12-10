import talib
import pandas as pd


class CandlesPatterns:
    """
    Detect all candlestick patterns using TA-Lib.
    """

    def __init__(self):
        self.result_df = pd.DataFrame(columns=['Pattern', 'Signal', 'Stoploss'])

    def detect_pattern(self, data: pd.DataFrame, pattern_function, pattern_name: str):
        """
        General method to detect a specific candlestick pattern.
        """
        # Calculate the pattern using TA-Lib
        pattern = pattern_function(
            data['open'].values,
            data['high'].values,
            data['low'].values,
            data['close'].values
        )

        # Identify bullish, bearish, or no pattern
        last_pattern_value = pattern[-1]
        if last_pattern_value > 0:
            signal = "Buy"
        elif last_pattern_value < 0:
            signal = "Sell"
        else:
            signal = "Flat"

        return {
            "Pattern": pattern_name,
            "Signal": signal,
            "Value": last_pattern_value
        }

    def doji(self, data: pd.DataFrame):
        '''
        Detect Doji Pattern.
        '''
        return self.detect_pattern(data, talib.CDLDOJI, "Doji")

    def dragonfly_doji(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLDRAGONFLYDOJI, "Dragonfly Doji")

    def gravestone_doji(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLGRAVESTONEDOJI, "Gravestone Doji")

    def engulfing(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLENGULFING, "Engulfing")

    def morning_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLMORNINGSTAR, "Morning Star")

    def evening_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLEVENINGSTAR, "Evening Star")

    def morning_doji_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLMORNINGDOJISTAR, "Morning Doji Star")

    def evening_doji_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLEVENINGDOJISTAR, "Evening Doji Star")

    def hammer(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLHAMMER, "Hammer")

    def inverted_hammer(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLINVERTEDHAMMER, "Inverted Hammer")

    def hanging_man(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLHANGINGMAN, "Hanging Man")

    def shooting_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLSHOOTINGSTAR, "Shooting Star")

    def marubozu(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLMARUBOZU, "Marubozu")

    def harami(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLHARAMI, "Harami")

    def harami_cross(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLHARAMICROSS, "Harami Cross")

    def spinning_top(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLSPINNINGTOP, "Spinning Top")

    def kicking(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLKICKING, "Kicking")

    def kicking_by_length(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLKICKINGBYLENGTH, "Kicking by Length")

    def tasuki_gap(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLTASUKIGAP, "Tasuki Gap")

    def gap_side_by_side_white(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLGAPSIDESIDEWHITE, "Gap Side By Side White")

    def counter_attack(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLCOUNTERATTACK, "Counterattack")

    def piercing(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLPIERCING, "Piercing")

    def dark_cloud_cover(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLDARKCLOUDCOVER, "Dark Cloud Cover")

    def tri_star(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLTRISTAR, "Tri Star")

    def on_neck(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLONNECK, "On Neck")

    def in_neck(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLINNECK, "In Neck")

    def thrusting(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLTHRUSTING, "Thrusting")

    def matching_low(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLMATCHINGLOW, "Matching Low")

    def three_black_crows(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDL3BLACKCROWS, "Three Black Crows")

    def three_white_soldiers(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDL3WHITESOLDIERS, "Three White Soldiers")

    def three_inside(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDL3INSIDE, "Three Inside")

    def three_outside(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDL3OUTSIDE, "Three Outside")

    def three_stars_in_south(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDL3STARSINSOUTH, "Three Stars in South")

    def advance_block(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLADVANCEBLOCK, "Advance Block")

    def stalled_pattern(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLSTALLEDPATTERN, "Stalled Pattern")

    def abandoned_baby(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLABANDONEDBABY, "Abandoned Baby")

    def unique_3_river(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLUNIQUE3RIVER, "Unique 3 River")

    def belt_hold(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLBELTHOLD, "Belt Hold")

    def separating_lines(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLSEPARATINGLINES, "Separating Lines")

    def upside_gap_two_crows(self, data: pd.DataFrame):
        return self.detect_pattern(data, talib.CDLUPSIDEGAP2CROWS, "Upside Gap Two Crows")
