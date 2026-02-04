# src/ingestao/ingestao_relacionamentos.py

from src.ingestao.base_ingestor import BaseIngestor
from src.servicos.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.servicos.corretor_imobiliaria_service import CorretorImobiliariaService

class IngestaoRelacionamentos(BaseIngestor):
    def __init__(self):
        self.ci = ConstrutoraImobiliariaService()
        self.cori = CorretorImobiliariaService()

    def carregar(self, fonte):
        return fonte

    def transformar(self, dados):
        return dados

    def salvar(self, dados):
        resultados = []
        for item in dados:
            if item["tipo"] == "construtora_imobiliaria":
                resultados.append(
                    self.ci.vincular(item["construtora_id"], item["imobiliaria_id"])
                )
            elif item["tipo"] == "corretor_imobiliaria":
                resultados.append(
                    self.cori.vincular(item["corretor_id"], item["imobiliaria_id"])
                )
        return resultados