import os
from openpyxl import Workbook

class MatchingExporterCompleto:

    def __init__(self, matching_service, lead_repository, empreendimento_repository):
        self.matching_service = matching_service
        self.lead_repository = lead_repository
        self.empreendimento_repository = empreendimento_repository

    def exportar_por_lead(self, lead_id: int, caminho_arquivo: str):
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

    def exportar_todos(self, pasta_destino: str):
        leads = self.lead_repository.consultar()
        if not leads:
            raise ValueError("Nenhum lead encontrado.")

        os.makedirs(pasta_destino, exist_ok=True)

        arquivos = []

        for lead in leads:
            matchings = self.matching_service.matching_repo.list_by_lead(lead.id)
            if not matchings:
                continue

            caminho = os.path.join(pasta_destino, f"lead_{lead.id}.xlsx")

            wb = Workbook()
            ws = wb.active
            ws.title = f"Lead {lead.id}"

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

            wb.save(caminho)
            arquivos.append(caminho)

        return arquivos
