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

    def __init__(self, mode="analyze", parent=None):
        super().__init__(parent)
        self.mode = mode

        ## Adicionar botões
        self.symbol = 'MSFT'
        self.period = '1y'
        self.interval = '1d'
    
    def run(self):
        try:
            if self.mode == "analyze":
                self.perform_analysis()
            elif self.mode == "optimize":
                self.optimize_metrics()
        except Exception as e:
            self.progress_text.emit(f"Erro durante a execução: {e}\n")

    def perform_analysis(self, symbol = str, interval = str, period = str):
        self.progress_text.emit("Iniciando análise...\n")
        self.progress_value.emit(0)

        from backend.datasources.yahoodata import DataHistory
        from backend.tecnical_analysis.trend_metrics import TrendMetrics
        from backend.tecnical_analysis.candles_patterns import CandlesPatterns
        
        dh = DataHistory()
        df = dh.get_yahoo_data_history(symbol=symbol, interval=interval, period=period)

        self.progress_text.emit("Calculando indicadores...\n")
        self.progress_value.emit(30)

        tm = TrendMetrics()
        tm.get_sma_bands(data=df, length=15, std_dev=1)
        tm.get_crossover(data=df, l1=25, l2=50, l3=200)
        tm.get_rsi(data=df, length=25, overbought=70, oversold=30)

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

    def optimize_metrics(self, asset_type = str, symbol = str, interval = str, period = str):
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
        self.ui.pushButton.clicked.connect(self.start_analysis)
        self.ui.pushButton_2.clicked.connect(self.pause_analysis)
        self.ui.pushButton_3.clicked.connect(self.stop_analysis)
        self.ui.pushButton_6.clicked.connect(self.start_optimization)

        # Configuração inicial
        self.analysis_thread = None
        self.paused = False

    def start_analysis(self):
        """Inicia a análise em uma thread separada."""
        self.log_message("Iniciando tarefa...\n")
        self.ui.label_4.setText("Iniciando análise...")
        self.ui.progressBar.setValue(0)
        self.analysis_thread = AnalysisThread(mode="analyze")
        self.analysis_thread.progress_text.connect(self.log_message)
        self.analysis_thread.progress_value.connect(self.update_progress)
        self.analysis_thread.dataframe_ready.connect(self.display_dataframe)
        self.analysis_thread.start()

    def start_optimization(self):
        """Inicia a calibração de métricas em uma thread separada."""
        self.log_message("Iniciando calibração de métricas...\n")
        self.ui.label_4.setText("Calibrando métricas...")
        self.ui.progressBar.setValue(0)
        self.analysis_thread = AnalysisThread(mode="optimize")
        self.analysis_thread.progress_text.connect(self.log_message)
        self.analysis_thread.progress_value.connect(self.update_progress)
        self.analysis_thread.dataframe_ready.connect(self.display_dataframe)
        self.analysis_thread.start()

    def pause_analysis(self):
        """Pausa a análise."""
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.paused = not self.paused
            if self.paused:
                self.log_message("Análise pausada.\n")
            else:
                self.log_message("Análise retomada.\n")
            
    def stop_analysis(self):
        """Para a análise."""
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.terminate()
            self.log_message("Análise parada.\n")

    def display_dataframe(self, df, table_type):
        """Exibe o DataFrame no QTableWidget correspondente."""
        if table_type == "trend_metrics":
            table_widget = self.ui.tableWidget
        elif table_type == "candle_patterns":
            table_widget = self.ui.tableWidget_2
        else:
            self.log_message("Tipo de tabela desconhecido.\n")
            return
        df = df.reset_index()

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
        self.ui.progressBar.setValue(value)

    def log_message(self, message):
        """Adiciona uma mensagem ao log e atualiza a label_4."""
        print(message)
        self.ui.label_4.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())

