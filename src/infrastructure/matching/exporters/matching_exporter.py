import os
from openpyxl import Workbook

class MatchingExporter:

    def __init__(self, matching_service, lead_repository, empreendimento_repository):
        self.matching_service = matching_service
        self.lead_repository = lead_repository
        self.empreendimento_repository = empreendimento_repository

    def exportar(self, lead_id: int, caminho_arquivo: str):
        lead = self.lead_repository.buscar_por_id(lead_id)
        if not lead:
            raise ValueError(f"Lead {lead_id} não encontrado.")

        matchings = self.matching_service.matching_repo.list_by_lead(lead_id)
        if not matchings:
            raise ValueError(f"Nenhum matching encontrado para o lead {lead_id}.")

        wb = Workbook()
        ws = wb.active
        ws.title = f"Lead {lead_id}"

        colunas = [
            "id_matching",
            "score",
            "reasons_json",
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

        for m in matchings:
            emp = self.empreendimento_repository.find_by_id(m.property_id)

            ws.append([
                m.id,
                m.score,
                str(m.reasons_json),
                m.created_at,
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
