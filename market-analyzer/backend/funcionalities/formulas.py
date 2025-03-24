import pandas as pd
import numpy as np

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