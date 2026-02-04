# src/ingestao/xls_parser.py

import pandas as pd
from pathlib import Path

class XLSParser:

    def ler(self, caminho, aba=None):
        caminho = Path(caminho)

        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        try:
            # Abre o arquivo Excel
            xls = pd.ExcelFile(caminho)

            # Se aba não for informada, pega a primeira
            if aba is None:
                aba = xls.sheet_names[0]

            # Lê a aba desejada
            df = pd.read_excel(
                xls,
                sheet_name=aba,
                dtype=str,
                keep_default_na=False
            )

            # Fecha o arquivo explicitamente
            xls.close()

            # Normaliza cabeçalhos
            df.columns = [
                col.strip()
                   .replace(" ", "")
                   .replace("\n", "")
                   .replace("\r", "")
                for col in df.columns
            ]

            # Converte para lista de dicts
            registros = df.to_dict(orient="records")

            # Remove linhas completamente vazias
            registros = [
                r for r in registros
                if any(str(v).strip() for v in r.values())
            ]

            return registros

        except Exception as e:
            # Garante que o arquivo será fechado mesmo em caso de erro
            try:
                xls.close()
            except:
                pass

            raise Exception(f"Erro ao ler arquivo XLS/XLSX: {e}")