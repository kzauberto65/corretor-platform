# src/ingestao/ingestao_corretor.py

from src.ingestao.base_ingestor import BaseIngestor
from src.servicos.corretor_service import CorretorService
from src.ingestao.normalizador import Normalizador

class IngestaoCorretor(BaseIngestor):
    def __init__(self):
        self.service = CorretorService()
        self.norm = Normalizador()

    def carregar(self, fonte):
        return fonte

    def transformar(self, dados):
        for d in dados:
            d["nome"] = self.norm.texto(d["nome"])
        return dados

    def salvar(self, dados):
        resultados = []
        for item in dados:
            c = self.service.criar_corretor(
                nome=item["nome"],
                telefone=item.get("telefone"),
                email=item.get("email"),
                creci=item.get("creci"),
                observacoes=item.get("observacoes")
            )
            resultados.append(c)
        return resultados