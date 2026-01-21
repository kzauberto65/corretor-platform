# src/ingestao/ingestao_unidade.py

from src.ingestao.base_ingestor import BaseIngestor
from src.servicos.unidade_service import UnidadeService
from src.ingestao.normalizador import Normalizador

class IngestaoUnidade(BaseIngestor):
    def __init__(self):
        self.service = UnidadeService()
        self.norm = Normalizador()

    def carregar(self, fonte):
        return fonte

    def transformar(self, dados):
        for d in dados:
            d["numero"] = self.norm.texto(d["numero"])
        return dados

    def salvar(self, dados):
        resultados = []
        for item in dados:
            unidade = self.service.criar_unidade(
                empreendimento_id=item["empreendimento_id"],
                numero=item["numero"],
                andar=item.get("andar"),
                area=item.get("area"),
                referencia_tipo=item.get("referencia_tipo"),
                preco=item.get("preco"),
                status=item.get("status")
            )
            resultados.append(unidade)
        return resultados