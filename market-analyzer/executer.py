import sys
import pandas as pd
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from frontend.interface import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

# Thread para executar a análise
class AnalysisThread(QThread):
    progress = pyqtSignal(str)  # Sinal para enviar atualizações para a interface
    dataframe_ready = pyqtSignal(object, str)  # Sinal para enviar o DataFrame processado

    def run(self):
        try:
            self.progress.emit("Iniciando análise...\n")

            from backend.datasources.yahoodata import DataHistory
            from backend.tecnical_analysis.trend_metrics import TrendMetrics
            from backend.tecnical_analysis.candles_patterns import CandlesPatterns

            dh = DataHistory()
            df = dh.get_yahoo_data_history('MSFT', '1y', '1d')

            tm = TrendMetrics()
            tm.get_sma_bands(data=df, length=15, std_dev=1)
            tm.get_crossover(data=df, l1=25, l2=50, l3=200)
            tm.get_rsi(data=df, length=25, overbought=70, oversold=30)

            self.progress.emit("Indicadores calculados: SMA Bands, Crossover, RSI.\n")
            self.dataframe_ready.emit(tm.result_df, "trend_metrics") 

            self.progress.emit("Iniciando deteção de padrões...\n")

            cm = CandlesPatterns()
            for candle_function in dir(cm):
                if (not candle_function.startswith("__") and
                        callable(getattr(cm, candle_function)) and
                        candle_function != "detect_pattern"):
                    pattern_function = getattr(cm, candle_function)
                    try:
                        candle_result = pattern_function(df)
                    except Exception as e:
                        self.progress.emit(f"Erro ao detectar padrão {candle_function}: {e}\n")

            self.progress.emit("Análise concluída!\n")
            self.dataframe_ready.emit(cm.result_candles_df, "candle_patterns")

        except Exception as e:
            self.progress.emit(f"Erro durante a execução: {e}\n")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar os botões aos métodos correspondentes
        self.ui.pushButton.clicked.connect(self.start_analysis)  # Botão "Run"
        self.ui.pushButton_2.clicked.connect(self.pause_analysis)  # Botão "Pause"
        self.ui.pushButton_3.clicked.connect(self.stop_analysis)  # Botão "Stop"

        # Configuração inicial
        self.analysis_thread = None
        self.paused = False

    def log_message(self, message):
        """Adiciona uma mensagem ao log."""
        print(message)
        self.ui.pushButton_5.setText(message)

    def start_analysis(self):
        """Inicia a análise em uma thread separada."""
        self.log_message("Iniciando tarefa...\n")
        self.analysis_thread = AnalysisThread()
        self.analysis_thread.progress.connect(self.log_message)
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
                    value = value.strftime("YY-mm-dd") 
                elif pd.isna(value):
                    value = ""
                table_widget.setItem(i, j, QTableWidgetItem(str(value)))

        self.log_message(f"Resultados exibidos na tabela {table_type}.\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())

