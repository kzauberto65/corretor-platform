import os
from datetime import datetime

class LoggerIngestao:
    def __init__(self):
        self.base_dir = "data/logs"
        os.makedirs(self.base_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.caminho_log = os.path.join(self.base_dir, f"ingestao_{timestamp}.log")

    def registrar(self, mensagem):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{timestamp}] {mensagem}\n"

        with open(self.caminho_log, "a", encoding="utf-8") as f:
            f.write(linha)