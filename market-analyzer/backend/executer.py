from datasources.yahoodata import DataHistory
from tecnical_analysis.trend_metrics import TrendMetrics
from tecnical_analysis.candles_patterns import CandlesPatterns

class Executer():
    def __init__(self) -> None:
        pass 

    def main(self):
        dh = DataHistory()
        data = dh.get_yahoo_data_history('MSFT','1y','1d')

        tm = TrendMetrics()
        tm.get_crossover()
        tm.get_sma_bands()
        tm.get_rsi()

        cm = CandlesPatterns()

        # Loop para detectar padrões
        for candle_function in dir(cm):
            if (not candle_function.startswith("__") and 
                callable(getattr(cm, candle_function)) and 
                candle_function != "detect_pattern"):
                pattern_function = getattr(cm, candle_function)
                try:
                    candle_result = pattern_function(data)
                except Exception as e:
                    print(f"Error detecting pattern {candle_function}: {e}")

if __name__ == "__main__":
    # Instantiate Executer and call main
    exec = Executer()
    exec.main()