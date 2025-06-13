import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

class Formulas():

    def __init__(self) -> None:
        self

    def get_yoy_metric(self, series):
        if isinstance(series, pd.Series):
            series = series.replace(0, np.nan).dropna()

            if len(series) >= 2:
                yoy_growth = ((series - series.shift(-1)) / series.shift(-1)) * 100
                yoy_growth = yoy_growth.dropna()
            else:
                yoy_growth = pd.Series("N/A", index=series.index)

        return yoy_growth

    def get_cagr_metric(self, series):
        if isinstance(series, pd.Series):
            series = pd.to_numeric(series, errors='coerce').dropna()

            if len(series) >= 2:
                start_value = series.iloc[-1]
                end_value = series.iloc[0]
                num_years = len(series) - 1

                if start_value != 0:
                    cagr = ((end_value / start_value) ** (1 / num_years)) - 1
                else:
                    cagr = "N/A"
            else:
                cagr = "N/A"
        else:
            cagr = "N/A"

        cagr_percent = cagr * 100 if cagr != "N/A" else "N/A"

        return cagr_percent
    

    def peak_detect(self, close, order):
        '''
        This function find the peaks of a timeframe    
        '''

        if len(close) < 5:
            return [], [], 0, 0, []

        if isinstance(close, pd.Series):
            close_np = close.values  # Converte apenas os valores se for uma série Pandas
        else:
            close_np = np.array(close)

        max_idx = list(argrelextrema(close_np, comparator=np.greater, order=order)[0])
        min_idx = list(argrelextrema(close_np, comparator=np.less, order=order)[0])

        idx = max_idx + min_idx + [len(close_np)-1]
        idx.sort()

        current_idx = idx[-5:]

        start = min(current_idx)
        end = max(current_idx)

        current_pat = close_np[current_idx]

        return current_idx, current_pat, start, end, idx
    
    def safe_round(self, value):
        try:
            return round(float(value), 2)
        except (ValueError, TypeError):
            return None
        

    def convert_string_milions(self, value):
        if pd.isna(value) or value == "-":
            return 0
        
        value = str(value).strip().upper()
        
        try:
            if value.endswith('M'):
                return int(float(value[:-1]) * 1_000_000)
            elif value.endswith('B'):
                return int(float(value[:-1]) * 1_000_000_000)
            elif value.endswith('K'):
                return int(float(value[:-1]) * 1_000)
            else:
                return float(value.replace(",", ""))
        except:
            return 0