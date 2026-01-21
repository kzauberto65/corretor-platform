# src/ingestao/ingestao_construtora.py

from src.ingestao.base_ingestor import BaseIngestor
from src.servicos.construtora_service import ConstrutoraService
from src.ingestao.normalizador import Normalizador

class IngestaoConstrutora(BaseIngestor):
    def __init__(self):
        self.service = ConstrutoraService()
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
            c = self.service.criar_construtora(
                nome=item["nome"],
                cnpj=item.get("cnpj"),
                contato=item.get("contato"),
                observacoes=item.get("observacoes")
            )
            resultados.append(c)
        return resultados