import os
import shutil
from datetime import datetime

class GerenciadorArquivos:
    def mover_para_processado(self, caminho_arquivo):
        destino = caminho_arquivo.replace("entrada", "processado")
        self._mover(caminho_arquivo, destino)

    def mover_para_erros(self, caminho_arquivo):
        destino = caminho_arquivo.replace("entrada", "erros")
        self._mover(caminho_arquivo, destino)

    def _mover(self, origem, destino):
        pasta_destino = os.path.dirname(destino)
        os.makedirs(pasta_destino, exist_ok=True)

        # adiciona timestamp para evitar sobrescrita
        base, ext = os.path.splitext(destino)
        destino = f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"

        shutil.move(origem, destino)