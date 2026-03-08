# ============================================================
# PARSER: XLSParser
# Camada: infrastructure/ingestao/
# Descrição: Lê arquivos XLS/XLSX e retorna lista de dicts.
#            Usado por todos os ingestores do projeto.
#            Normaliza cabeçalhos e remove linhas vazias.
#
# Método principal: parse() — padrão usado por todos os ingestores.
#   (alias ler() mantido por retrocompatibilidade)
#
# Dependência: pandas + openpyxl
#   pip install pandas openpyxl
# ============================================================

import pandas as pd
from pathlib import Path


class XLSParser:
    """Parser de arquivos Excel para lista de dicts.

    Normaliza cabeçalhos: remove espaços, quebras de linha e
    caracteres especiais para garantir mapeamento correto com
    os campos dos DTOs.

    Todos os valores são lidos como string para evitar conversões
    automáticas incorretas do pandas (ex: 1.0 em vez de 1).
    A conversão de tipo é responsabilidade do ingestor concreto.
    """

    def parse(self, caminho: str, aba: str = None) -> list[dict]:
        """Lê um arquivo XLS/XLSX e retorna lista de dicts.

        Args:
            caminho: caminho para o arquivo Excel
            aba: nome da aba a ler (default: primeira aba)

        Returns:
            Lista de dicts onde cada dict é uma linha da planilha.
            Chaves = cabeçalhos normalizados, valores = strings.

        Raises:
            FileNotFoundError: se o arquivo não existir
            Exception: se houver erro na leitura do arquivo
        """
        return self.ler(caminho, aba)

    def ler(self, caminho: str, aba: str = None) -> list[dict]:
        """Alias de parse() — mantido para retrocompatibilidade.
        Preferir o uso de parse() em código novo."""
        caminho = Path(caminho)

        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        xls = None
        try:
            xls = pd.ExcelFile(caminho)

            # Usa primeira aba se não informada
            if aba is None:
                aba = xls.sheet_names[0]

            # Lê como string — conversão de tipos é papel do ingestor
            df = pd.read_excel(
                xls,
                sheet_name=aba,
                dtype=str,
                keep_default_na=False   # evita "NaN" como string
            )

            xls.close()

            # Normaliza cabeçalhos: remove espaços, newlines e caracteres invisíveis
            # Ex: "Nome do Imóvel\n" → "NomeDoImóvel" → mapeado via alias no ingestor
            df.columns = [
                col.strip()
                   .replace(" ", "_")   # espaço → underscore (snake_case)
                   .replace("\n", "")
                   .replace("\r", "")
                   .lower()             # lowercase para matching consistente
                for col in df.columns
            ]

            # Converte para lista de dicts
            registros = df.to_dict(orient="records")

            # Remove linhas completamente vazias
            registros = [
                r for r in registros
                if any(str(v).strip() for v in r.values())
            ]

            print(f"[XLSParser] {len(registros)} linha(s) lida(s) da aba '{aba}' em '{caminho.name}'")
            return registros

        except FileNotFoundError:
            raise
        except Exception as e:
            if xls:
                try:
                    xls.close()
                except Exception:
                    pass
            raise Exception(f"[XLSParser] Erro ao ler '{caminho}': {e}")

    def listar_abas(self, caminho: str) -> list[str]:
        """Retorna lista de abas disponíveis no arquivo.
        Útil para debug e quando a planilha tem múltiplas abas."""
        caminho = Path(caminho)
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        xls = pd.ExcelFile(caminho)
        abas = xls.sheet_names
        xls.close()
        return abas