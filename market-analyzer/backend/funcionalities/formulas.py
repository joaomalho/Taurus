import pandas as pd

class Formulas():

    def __init__(self) -> None:
        self

    def get_yoy_metric(self, series):
        if isinstance(series, pd.Series):
            yoy_growth = ((series - series.shift(-1)) / series.shift(-1)) * 100
            yoy_growth = yoy_growth.dropna()
            
        return yoy_growth
    
    def get_cagr_metric(self, series):
        series = series.dropna()
        if len(series) >= 2:
            start_value = series.iloc[-1]
            end_value = series.iloc[0]
            num_years = len(series) - 1
            cagr = ((end_value / start_value) ** (1 / num_years)) - 1

        cagr_percent = cagr * 100 if cagr != "N/A" else "N/A"

        return cagr_percent