# src/infrastructure/ia/exporters/ia_exporter.py

import os
import json
from openpyxl import Workbook


class IAExporter:

    def __init__(self, ia_service, lead_repository, empreendimento_repository):
        self.ia_service = ia_service
        self.lead_repository = lead_repository
        self.empreendimento_repository = empreendimento_repository

    def exportar(self, lead_id: int, caminho_arquivo: str):
        lead = self.lead_repository.buscar_por_id(lead_id)
        if not lead:
            raise ValueError(f"Lead {lead_id} não encontrado.")

        ia_results = self.ia_service.ia_repo.list_by_lead(lead_id)
        if not ia_results:
            raise ValueError(f"Nenhum resultado de IA encontrado para o lead {lead_id}.")

        wb = Workbook()
        ws = wb.active
        ws.title = f"Lead {lead_id}"

        colunas = [
            "id_ia",
            "similarity",
            "conversion_score",
            "reasons_json",
            "created_at",
            "id_empreendimento",
            "nome_empreendimento",
            "endereco",
            "bairro",
            "cidade",
            "preco",
            "tipologia"
        ]

        ws.append(colunas)

        for r in ia_results:
            emp = self.empreendimento_repository.find_by_id(r.property_id)

            ws.append([
                r.id,
                r.similarity,
                r.conversion_score,
                json.dumps(r.reasons_json, ensure_ascii=False),
                r.created_at,
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
