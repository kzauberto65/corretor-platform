# src/infrastructure/mailing/exporters/mailing_exporter.py

import os
from openpyxl import Workbook
from src.application.mailing.services.mailing_service import MailingService


class MailingExporterCompleto:

    def __init__(self, service: MailingService):
        self.service = service

    def exportar(self, caminho_arquivo: str):
        dados = self.service.consultar()

        wb = Workbook()
        ws = wb.active
        ws.title = "Mailing Completo"

        # Cabeçalhos (todas as colunas)
        colunas = [
            "id", "nome", "email", "telefone", "origem", "tags",
            "data_ingestao", "fonte_arquivo",
            "valido", "motivo_invalidacao", "hash_unico",
            "sexo", "data_nascimento", "idade", "estado_civil", "nacionalidade",
            "profissao", "empresa", "cargo", "renda_mensal", "faixa_renda", "escolaridade",
            "cep", "logradouro", "numero", "complemento", "bairro", "cidade", "estado", "pais",
            "intencao", "tipo_imovel", "faixa_preco", "preco_min", "preco_max",
            "quartos", "vagas", "metragem_min", "metragem_max",
            "bairro_interesse", "cidade_interesse", "urgencia", "motivo",
            "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
            "primeiro_contato", "ultimo_contato", "canal_preferido", "score_mailing",
            "criado_em", "atualizado_em"
        ]

        ws.append(colunas)

        # Linhas
        for item in dados:
            ws.append([getattr(item, c) for c in colunas])

        # Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

        wb.save(caminho_arquivo)
        return caminho_arquivo
