# src/infrastructure/mailing/exporters/mailing_exporter.py

import os
from openpyxl import Workbook
from src.application.mailing.services.mailing_service import MailingService


class MailingExporterResumido:

    def __init__(self, service: MailingService):
        self.service = service

    def exportar(self, caminho_arquivo: str):
        dados = self.service.consultar()

        wb = Workbook()
        ws = wb.active
        ws.title = "Mailing Resumido"

        # Colunas essenciais
        colunas = [
            "id",
            "nome",
            "email",
            "telefone",
            "origem",
            "cidade",
            "estado",
            "intencao",
            "tipo_imovel",
            "faixa_preco",
            "score_mailing"
        ]

        ws.append(colunas)

        for item in dados:
            ws.append([getattr(item, c) for c in colunas])

        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

        wb.save(caminho_arquivo)
        return caminho_arquivo
