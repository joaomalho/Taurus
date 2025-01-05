import sys
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit

# Thread para executar a análise
class AnalysisThread(QThread):
    progress = pyqtSignal(str)  # Sinal para enviar atualizações para a interface

    def run(self):
        try:
            self.progress.emit("Iniciando análise...\n")

            # Simula a execução do backend
            from datasources.yahoodata import DataHistory
            from tecnical_analysis.trend_metrics import TrendMetrics
            from tecnical_analysis.candles_patterns import CandlesPatterns

            dh = DataHistory()
            df = dh.get_yahoo_data_history('MSFT', '1y', '1d')

            tm = TrendMetrics()
            tm.get_sma_bands(data=df, length=15, std_dev=1)
            tm.get_crossover(data=df, l1=25, l2=50, l3=200)
            tm.get_rsi(data=df, length=25, overbought=70, oversold=30)

            print('------------- Results df -------------\n\n',tm.result_df,'\n\n------------- ')

            print('------------- Results Crossover -------------\n\n',tm.crossover_info,'\n\n------------- ')

            print('------------- Results Bollinger Bands -------------\n\n',tm.sma_bands_info,'\n\n------------- ')

            print('------------- Results RSI -------------\n\n',tm.rsi_info,'\n\n------------- ')
            
            self.progress.emit("Indicadores calculados: SMA Bands, Crossover, RSI.\n")

            cm = CandlesPatterns()
            for candle_function in dir(cm):
                if (not candle_function.startswith("__") and
                    callable(getattr(cm, candle_function)) and
                    candle_function != "detect_pattern"):
                    pattern_function = getattr(cm, candle_function)
                    try:
                        candle_result = pattern_function(df)
                        self.progress.emit(f"Padrão {candle_function}: {candle_result}\n")
                    except Exception as e:
                        self.progress.emit(f"Erro ao detectar padrão {candle_function}: {e}\n")

            self.progress.emit("Análise concluída!\n")

        except Exception as e:
            self.progress.emit(f"Erro durante a execução: {e}\n")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 600, 400)

        # Área de log
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)

        # Botão para iniciar análise
        self.start_button = QPushButton("Iniciar Análise", self)
        self.start_button.clicked.connect(self.start_analysis)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.log_area)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def log_message(self, message):
        """Adiciona uma mensagem ao log."""
        self.log_area.append(message)

    def start_analysis(self):
        """Inicia a análise em uma thread separada."""
        self.start_button.setEnabled(False)
        self.log_message("Iniciando tarefa...\n")

        # Criar e iniciar a thread
        self.analysis_thread = AnalysisThread()
        self.analysis_thread.progress.connect(self.log_message)
        self.analysis_thread.finished.connect(self.task_completed)
        self.analysis_thread.start()

    def task_completed(self):
        """Reabilita o botão após a conclusão da análise."""
        self.start_button.setEnabled(True)
        self.log_message("Tarefa concluída.\n")

# Inicializar a aplicação
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

