# src/ingestao/ingestao_empreendimento.py

from src.ingestao.base_ingestor import BaseIngestor
from src.servicos.empreendimento_service import EmpreendimentoService
from src.ingestao.normalizador import Normalizador

class IngestaoEmpreendimento(BaseIngestor):
    def __init__(self):
        self.service = EmpreendimentoService()
        self.norm = Normalizador()

    def carregar(self, fonte):
        return fonte  # já vem como lista de dicts

    def transformar(self, dados):
        for d in dados:
            d["bairro"] = self.norm.texto(d["bairro"])
            d["cidade"] = self.norm.texto(d["cidade"])
            d["estado"] = self.norm.texto(d["estado"])
            d["produto"] = self.norm.texto(d["produto"])
        return dados

    def salvar(self, dados):
        resultados = []
        for item in dados:
            emp = self.service.criar_empreendimento(
                regiao=item["regiao"],
                bairro=item["bairro"],
                cidade=item["cidade"],
                estado=item["estado"],
                produto=item["produto"],
                endereco=item.get("endereco"),
                data_entrega=item.get("data_entrega"),
                status_entrega=item.get("status_entrega"),
                tipo=item.get("tipo"),
                descricao=item.get("descricao")
            )
            resultados.append(emp)
        return resultados