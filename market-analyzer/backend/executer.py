import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import threading  # Para manter a interface responsiva
from datasources.yahoodata import DataHistory
from tecnical_analysis.trend_metrics import TrendMetrics
from tecnical_analysis.candles_patterns import CandlesPatterns

class Executer:
    def __init__(self, log_callback):
        self.log_callback = log_callback

    def main(self):
        try:
            self.log_callback("Iniciando análise...\n")
            
            dh = DataHistory()
            data = dh.get_yahoo_data_history('MSFT', '1y', '1d')

            tm = TrendMetrics()
            tm.get_crossover()
            tm.get_sma_bands()
            tm.get_rsi()
            self.log_callback("Indicadores calculados: SMA Bands, Crossover, RSI.\n")

            cm = CandlesPatterns()
            for candle_function in dir(cm):
                if (not candle_function.startswith("__") and 
                    callable(getattr(cm, candle_function)) and 
                    candle_function != "detect_pattern"):
                    pattern_function = getattr(cm, candle_function)
                    try:
                        candle_result = pattern_function(data)
                        self.log_callback(f"Padrão {candle_function}: {candle_result}\n")
                    except Exception as e:
                        self.log_callback(f"Erro ao detectar padrão {candle_function}: {e}\n")
            
            self.log_callback("Análise concluída!\n")

        except Exception as e:
            self.log_callback(f"Erro durante a execução: {e}\n")

class TaskManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Task Manager")

        self.set_border_width(10)
        self.set_default_size(600, 400)

        # Layout principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Botão para iniciar análise
        self.start_button = Gtk.Button(label="Iniciar Análise")
        self.start_button.connect("clicked", self.start_task)
        vbox.pack_start(self.start_button, False, False, 0)

        # Área de log
        self.log_textview = Gtk.TextView()
        self.log_textview.set_editable(False)
        self.log_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        vbox.pack_start(self.log_textview, True, True, 0)

        # Barra de rolagem para o log
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.log_textview)
        vbox.pack_start(scroll, True, True, 0)

    def log_message(self, message):
        """Adiciona uma mensagem ao log."""
        buffer = self.log_textview.get_buffer()
        buffer.insert(buffer.get_end_iter(), message)

    def start_task(self, widget):
        """Inicia a execução do backend em uma thread separada."""
        self.start_button.set_sensitive(False)
        self.log_message("Iniciando tarefa...\n")

        # Criar thread para executar o backend
        thread = threading.Thread(target=self.run_backend)
        thread.daemon = True
        thread.start()

    def run_backend(self):
        """Executa o backend e atualiza a interface."""
        executer = Executer(log_callback=self.log_message)
        executer.main()

        # Reabilitar o botão após a conclusão
        GLib.idle_add(self.start_button.set_sensitive, True)

if __name__ == "__main__":
    win = TaskManager()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

