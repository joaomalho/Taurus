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
        
        print("Yahoo Data History:")
        print(data)


if __name__ == "__main__":
    # Instantiate Executer and call main
    exec = Executer()
    exec.main()