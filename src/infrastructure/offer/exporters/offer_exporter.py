import os
from openpyxl import Workbook

class OfferExporter:

    def __init__(self, offer_service, lead_repository, empreendimento_repository):
        self.offer_service = offer_service
        self.lead_repository = lead_repository
        self.empreendimento_repository = empreendimento_repository

    def exportar(self, lead_id: int, caminho_arquivo: str):
        lead = self.lead_repository.buscar_por_id(lead_id)
        if not lead:
            raise ValueError(f"Lead {lead_id} não encontrado.")

        ofertas = self.offer_service.offer_repository.find_by_lead(lead_id)
        if not ofertas:
            raise ValueError(f"Nenhuma oferta encontrada para o lead {lead_id}.")

        wb = Workbook()
        ws = wb.active
        ws.title = f"Lead {lead_id}"

        colunas = [
            "id_oferta",
            "score",
            "rationale",
            "criado_em",
            "id_empreendimento",
            "nome_empreendimento",
            "endereco",
            "bairro",
            "cidade",
            "preco",
            "tipologia"
        ]

        ws.append(colunas)

        for oferta in ofertas:
            emp = self.empreendimento_repository.find_by_id(oferta.empreendimento_id)

            ws.append([
                oferta.id,
                oferta.score,
                oferta.rationale,
                oferta.created_at,
                emp.id,
                emp.nome,
                emp.endereco,
                emp.bairro,
                emp.cidade,
                emp.preco,
                emp.tipologia
            ])

        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        wb.save(caminho_arquivo)

        return caminho_arquivo
