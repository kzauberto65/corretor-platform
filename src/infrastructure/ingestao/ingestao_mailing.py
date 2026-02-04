# src/infrastructure/ingestao/ingestao_mailing.py

from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.normalizador import Normalizador
from src.application.mailing.services.mailing_service import MailingService
from src.infrastructure.mailing.repositories.mailing_repository import MailingRepository
from src.domain.mailing.dto.mailing_input_dto import MailingInputDTO
import os
print(">>> ARQUIVO EXECUTADO:", os.path.abspath(__file__))
import pandas as pd
import shutil
from pandas import Timestamp, NaT
import numpy as np
from datetime import datetime


class IngestaoMailing(BaseIngestor):
    def __init__(self):
        super().__init__()
        self.service = MailingService(MailingRepository())
        self.norm = Normalizador()

    def carregar(self, fonte):
        return fonte

    def transformar(self, dados):
        dtos = []

        for d in dados:

            # 🔥 Função universal para tratar QUALQUER tipo antes do normalizador
            def tratar_valor(valor):

                # None
                if valor is None:
                    return None

                # NaT (Not a Time)
                if valor is NaT:
                    return None

                # Pandas Timestamp
                if isinstance(valor, Timestamp):
                    return valor.strftime("%Y-%m-%d")

                # numpy datetime64
                if isinstance(valor, np.datetime64):
                    return str(pd.to_datetime(valor).date())

                # numpy numbers
                if isinstance(valor, (np.int64, np.float64)):
                    return str(valor)

                # Qualquer outro tipo estranho → vira string
                return str(valor)

            campos_basicos = ["nome", "email", "telefone", "origem", "tags"]
            for campo in campos_basicos:
                valor = tratar_valor(d.get(campo))
                d[campo] = self.norm.texto(valor)

            campos_extra = [
                "sexo", "estado_civil", "nacionalidade", "profissao", "empresa",
                "cargo", "faixa_renda", "escolaridade", "cep", "logradouro",
                "numero", "complemento", "bairro", "cidade", "estado", "pais",
                "intencao", "tipo_imovel", "faixa_preco", "bairro_interesse",
                "cidade_interesse", "urgencia", "motivo", "utm_source",
                "utm_medium", "utm_campaign", "utm_term", "utm_content",
                "canal_preferido", "data_nascimento", "primeiro_contato",
                "ultimo_contato"
            ]

            for campo in campos_extra:
                valor = tratar_valor(d.get(campo))
                d[campo] = self.norm.texto(valor)

            dto = MailingInputDTO(**d)
            dtos.append(dto)

        return dtos

    def salvar(self, dados):
        resultados = []
        for dto in dados:
            criado = self.service.cadastrar(dto)
            resultados.append(criado)
        return resultados

    def executar_ingestao(self):
        print(">>> VERSÃO NOVA DO INGESTOR RODANDO <<<")
        pasta_entrada = "data/entrada/mailing"
        pasta_processado = "data/processado/mailing"
        pasta_erros = "data/erros/mailing"

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

            # gera timestamp para renomear
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome, ext = os.path.splitext(arquivo)
            novo_nome = f"{nome}_{timestamp}{ext}"

            try:
                df = pd.read_excel(caminho)
                dados = df.to_dict(orient="records")

                carregado = self.carregar(dados)
                transformado = self.transformar(carregado)
                self.salvar(transformado)

                # move com nome novo
                shutil.move(caminho, os.path.join(pasta_processado, novo_nome))
                print(f"Arquivo movido para processado como {novo_nome}")

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

                # renomeia também para erros
                shutil.move(caminho, os.path.join(pasta_erros, novo_nome))
                print(f"Arquivo movido para erros como {novo_nome}")


if __name__ == "__main__":
    ing = IngestaoMailing()
    ing.executar_ingestao()
