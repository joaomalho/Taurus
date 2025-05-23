import sys
import pandas as pd
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from frontend.interface import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

# Thread para executar a análise
class AnalysisThread(QThread):
    progress_text = pyqtSignal(str)
    progress_value = pyqtSignal(int)
    dataframe_ready = pyqtSignal(object, str)

    def __init__(self, mode:str, ticker:str, period:str, interval:str):
        super().__init__()
        self.mode = mode

        ## Adicionar botões
        self.ticker = ticker
        self.period = period
        self.interval = interval
    
    def run(self):
        try:
            if self.mode == "analyze":
                self.perform_analysis(self.ticker, self.interval, self.period)
            elif self.mode == "optimize":
                self.optimize_metrics("stock", self.ticker, self.interval, self.period)
        except Exception as e:
            self.progress_text.emit(f"Erro durante a execução: {e}\n")

    def perform_analysis(self, symbol : str, interval : str, period : str):
        self.progress_text.emit("Iniciando análise...\n")
        self.progress_value.emit(0)

        from backend.datasources.yahoodata import DataHistoryYahoo
        from backend.tecnical_analysis.trend_metrics import TrendMetrics
        from backend.tecnical_analysis.candles_patterns import CandlesPatterns
        
        dh = DataHistoryYahoo()
        df = dh.get_yahoo_data_history(symbol=symbol, interval=interval, period=period)

        self.progress_text.emit("Calculando indicadores...\n")
        self.progress_value.emit(30)

        tm = TrendMetrics()
        tm.get_sma_bands(data=df, length=15, std_dev=1)
        tm.get_crossover(data=df, fastperiod=25, mediumperiod=50, slowperiod=200)
        tm.get_rsi(data=df, length=25, overbought=70, oversold=30)
        tm.get_adx(data=df, length=25)
        tm.get_macd(data=df, fastperiod=12, slowperiod=26, signalperiod=9)

        self.progress_text.emit("Indicadores calculados: SMA Bands, Crossover, RSI.\n")
        self.progress_value.emit(60)
        self.dataframe_ready.emit(tm.result_df, "trend_metrics") 

        self.progress_text.emit("Iniciando deteção de padrões...\n")
        cm = CandlesPatterns()
        for candle_function in dir(cm):
            if (not candle_function.startswith("__") and
                callable(getattr(cm, candle_function)) and
                candle_function != "detect_pattern"):
                pattern_function = getattr(cm, candle_function)
                try:
                    candle_result = pattern_function(df)
                except Exception as e:
                    self.progress_text.emit(f"Erro ao detectar padrão {candle_function}: {e}\n")

        self.progress_text.emit("Análise concluída!\n")
        self.progress_value.emit(100)
        self.dataframe_ready.emit(cm.result_candles_df, "candle_patterns")

    def optimize_metrics(self, asset_type : str, symbol : str, interval : str, period : str):
        """Executa a calibração de métricas."""
        self.progress_text.emit("Iniciando calibração de métricas...\n")
        self.progress_value.emit(0)

        from backend.funcionalities.optimizer import ParamsOptimization
        optimizer = ParamsOptimization()

        optimizer.optimize(asset_type='stock', symbol=symbol, period=period, interval=interval)

        self.progress_text.emit("Calibração de crossover concluída.\n")
        self.dataframe_ready.emit(optimizer.crossover_results, "trend_metrics")

        self.progress_text.emit("Calibração de Bollinger Bands concluída.\n")
        self.dataframe_ready.emit(optimizer.bbands_results, "candle_patterns")

        self.progress_text.emit("Calibração concluída!\n")
        self.progress_value.emit(100)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar os botões aos métodos correspondentes
        self.ui.pushButton_run.clicked.connect(self.start_analysis)
        self.ui.pushButton_stop.clicked.connect(self.stop_analysis)
        self.ui.pushButton_reset.clicked.connect(self.reset_analysis)
        self.ui.pushButton_autoCali.clicked.connect(self.start_optimization)

        # Configuração inicial
        self.analysis_thread = None
        self.paused = False

    def start_analysis(self):
        """Inicia a análise em uma thread separada."""
        self.log_message("Iniciando tarefa...\n")
        self.ui.label_loading.setText("Iniciando análise...")
        self.ui.progressBar_main.setValue(0)
        self.analysis_thread = AnalysisThread(mode="analyze", ticker='SPY', period= '1y', interval = '1d')
        self.analysis_thread.progress_text.connect(self.log_message)
        self.analysis_thread.progress_value.connect(self.update_progress)
        self.analysis_thread.dataframe_ready.connect(self.display_dataframe)
        self.analysis_thread.start()

    def start_optimization(self):
        """Inicia a calibração de métricas em uma thread separada."""
        self.log_message("Iniciando calibração de métricas...\n")
        self.ui.label_loading.setText("Calibrando métricas...")
        self.ui.progressBar_main.setValue(0)
        self.analysis_thread = AnalysisThread(mode="optimize", ticker='SPY', period= '1y', interval = '1d')
        self.analysis_thread.progress_text.connect(self.log_message)
        self.analysis_thread.progress_value.connect(self.update_progress)
        self.analysis_thread.dataframe_ready.connect(self.display_dataframe)
        self.analysis_thread.start()

    def reset_analysis(self):
       pass
            
    def stop_analysis(self):
        """Para a análise."""
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.terminate()
            self.log_message("Análise parada.\n")

    def display_dataframe(self, df, table_type):
        """Exibe o DataFrame no QTableWidget correspondente."""
        if table_type == "trend_metrics":
            table_widget = self.ui.tableWidget_trendMetrics
        elif table_type == "candle_patterns":
            table_widget = self.ui.tableWidget_candlePat
        else:
            self.log_message("Tipo de tabela desconhecido.\n")
            return
        df = df.reset_index(drop=True)

        table_widget.setRowCount(len(df))
        table_widget.setColumnCount(len(df.columns))
        table_widget.setHorizontalHeaderLabels(df.columns)

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                if isinstance(value, pd.Timestamp):
                    value = value.strftime("%Y-%m-%d") 
                elif pd.isna(value):
                    value = ""
                table_widget.setItem(i, j, QTableWidgetItem(str(value)))

    def update_progress(self, value):
        """Atualiza o valor da barra de progresso."""
        self.ui.progressBar_main.setValue(value)

    def log_message(self, message):
        """Adiciona uma mensagem ao log e atualiza a label_4."""
        print(message)
        self.ui.label_loading.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())

