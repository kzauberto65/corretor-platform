# src/ingestao/ingestao_imobiliaria.py

from src.ingestao.base_ingestor import BaseIngestor
from src.servicos.imobiliaria_service import ImobiliariaService
from src.ingestao.normalizador import Normalizador

class IngestaoImobiliaria(BaseIngestor):
    def __init__(self):
        self.service = ImobiliariaService()
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
            im = self.service.criar_imobiliaria(
                nome=item["nome"],
                cnpj=item.get("cnpj"),
                contato=item.get("contato"),
                observacoes=item.get("observacoes")
            )
            resultados.append(im)
        return resultados