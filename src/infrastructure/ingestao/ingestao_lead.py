from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.normalizador import Normalizador
from src.application.lead.services.lead_service import LeadService
from src.infrastructure.lead.repositories.lead_repository import LeadRepository
from src.domain.lead.dto.lead_input_dto import LeadInputDTO

import os
import pandas as pd
import shutil
from pandas import Timestamp, NaT
import numpy as np
from datetime import datetime


class IngestaoLead(BaseIngestor):
    def __init__(self):
        super().__init__()
        self.service = LeadService(LeadRepository())
        self.norm = Normalizador()

    def carregar(self, fonte):
        return fonte

    def transformar(self, dados):
        dtos = []

        for d in dados:

            # Cria o DTO bruto
            dto = LeadInputDTO(**d)

            # Função universal para tratar tipos antes da normalização
            def tratar_valor(valor):

                if valor is None:
                    return None

                if valor is NaT:
                    return None

                if isinstance(valor, Timestamp):
                    return valor.strftime("%Y-%m-%d")

                if isinstance(valor, np.datetime64):
                    return str(pd.to_datetime(valor).date())

                if isinstance(valor, (np.int64, np.float64)):
                    return str(valor)

                return str(valor)

            # Normaliza campo a campo diretamente no DTO
            for campo, valor in dto.__dict__.items():

                valor_tratado = tratar_valor(valor)

                # Normaliza apenas strings
                if isinstance(valor_tratado, str):
                    setattr(dto, campo, self.norm.texto(valor_tratado))
                else:
                    setattr(dto, campo, valor_tratado)

            dtos.append(dto)

        return dtos


    def salvar(self, dados):
        resultados = []
        for dto in dados:
            criado = self.service.cadastrar(dto)
            resultados.append(criado)
        return resultados

    def executar_ingestao(self):
        print(">>> INGESTÃO DE LEADS RODANDO <<<")

        pasta_entrada = "data/entrada/lead"
        pasta_processado = "data/processado/lead"
        pasta_erros = "data/erros/lead"

        os.makedirs(pasta_entrada, exist_ok=True)
        os.makedirs(pasta_processado, exist_ok=True)
        os.makedirs(pasta_erros, exist_ok=True)

        arquivos = [
            f for f in os.listdir(pasta_entrada)
            if f.lower().endswith((".xlsx", ".xls"))
        ]

        if not arquivos:
            print("Nenhum arquivo encontrado para ingestão.")
            return

        for arquivo in arquivos:
            caminho = os.path.join(pasta_entrada, arquivo)
            print(f"\nProcessando: {arquivo}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome, ext = os.path.splitext(arquivo)
            novo_nome = f"{nome}_{timestamp}{ext}"

            try:
                df = pd.read_excel(caminho)
                dados = df.to_dict(orient="records")

                carregado = self.carregar(dados)
                transformado = self.transformar(carregado)
                self.salvar(transformado)

                shutil.move(caminho, os.path.join(pasta_processado, novo_nome))
                print(f"Arquivo movido para processado como {novo_nome}")

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")
                shutil.move(caminho, os.path.join(pasta_erros, novo_nome))
                print(f"Arquivo movido para erros como {novo_nome}")


if __name__ == "__main__":
    ing = IngestaoLead()
    ing.executar_ingestao()
