# ============================================================
# NORMALIZADOR: Normalizador
# Camada: infrastructure/ingestao/
# Descrição: Utilitário de limpeza e normalização de dados brutos
#            vindos de planilhas, APIs ou formulários.
#            Usado pelos ingestores para sanitizar valores antes
#            de montar os DTOs.
#
# ATENÇÃO: este normalizador é para uso nos INGESTORES.
#          Normalização de domínio (regras de negócio) fica nos
#          Normalizers de cada módulo (ex: EmpreendimentoNormalizer).
# ============================================================

import re
import unicodedata
from datetime import datetime


class Normalizador:

    # ----------------------------------------------------------
    # TEXTOS
    # ----------------------------------------------------------

    def texto(self, valor) -> str | None:
        """Limpeza básica de string.
        Trata NaN/NaT do pandas, Timestamps e strings vazias."""
        if valor is None:
            return None

        # Detecta valores especiais do pandas antes de converter
        v_str = str(valor).strip().lower()
        if v_str in ("nan", "nat", "none", ""):
            return None

        # Se for Timestamp pandas (ex: célula de data lida como objeto)
        if hasattr(valor, "strftime"):
            return valor.strftime("%Y-%m-%d")

        v = str(valor).strip()
        return v if v.lower() not in ("nan", "none", "") else None

    def texto_titulo(self, valor) -> str | None:
        """Retorna texto em Title Case. Ex: 'são paulo' → 'São Paulo'."""
        v = self.texto(valor)
        return v.title() if v else None

    def texto_busca(self, valor) -> str | None:
        """Normaliza texto para uso em queries SQL (LIKE, comparações).
        Remove acentos e converte para minúsculas.
        NÃO usar para persistência — destrói acentos."""
        v = self.texto(valor)
        if not v:
            return None
        # Remove diacríticos (acentos)
        v = unicodedata.normalize("NFD", v)
        v = "".join(c for c in v if unicodedata.category(c) != "Mn")
        return v.lower()

    # ----------------------------------------------------------
    # NÚMEROS
    # ----------------------------------------------------------

    def numero(self, valor) -> str | None:
        """Retorna valor numérico como string limpa.
        Usado quando o destino é um campo TEXT no banco."""
        v = self.texto(valor)
        return v if v else None

    def inteiro(self, valor) -> int | None:
        """Converte para int. Aceita strings com vírgula decimal ('2,0').
        Retorna None se inválido."""
        v = self.texto(valor)
        if not v:
            return None
        try:
            return int(float(v.replace(",", ".")))
        except (ValueError, TypeError):
            return None

    def flutuante(self, valor) -> float | None:
        """Converte para float. Aceita vírgula como separador decimal.
        Retorna None se inválido."""
        v = self.texto(valor)
        if not v:
            return None
        try:
            return float(v.replace(",", "."))
        except (ValueError, TypeError):
            return None

    # ----------------------------------------------------------
    # MOEDA
    # ----------------------------------------------------------

    def moeda(self, valor) -> float | None:
        """Converte valor monetário para float.
        Aceita formatos: 'R$ 1.200.000,00', '1200000.00', '1.200.000'.
        Retorna None se inválido."""
        v = self.texto(valor)
        if not v:
            return None
        # Remove símbolo e espaços
        v = v.replace("R$", "").replace(" ", "")
        # Trata separador de milhar (.) e decimal (,)
        # Ex: '1.200.000,00' → '1200000.00'
        if "," in v:
            v = v.replace(".", "").replace(",", ".")
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    # ----------------------------------------------------------
    # DATAS
    # ----------------------------------------------------------

    def data(self, valor) -> str | None:
        """Converte data para formato ISO YYYY-MM-DD.
        Aceita formatos comuns de planilha: DD/MM/YYYY, DD-MM-YYYY,
        YYYY-MM-DD, DD/MM/YY.
        Retorna o valor original como string se formato não reconhecido."""
        v = self.texto(valor)
        if not v:
            return None

        formatos = [
            "%d/%m/%Y",     # 31/12/2025
            "%d-%m-%Y",     # 31-12-2025
            "%Y-%m-%d",     # 2025-12-31 (ISO — já correto)
            "%d/%m/%y",     # 31/12/25
        ]

        for fmt in formatos:
            try:
                return datetime.strptime(v, fmt).date().isoformat()
            except ValueError:
                continue

        # Retorna original se não reconhecido — não descarta o dado
        return v

    # ----------------------------------------------------------
    # DOCUMENTOS
    # ----------------------------------------------------------

    def limpar_cnpj(self, valor) -> str | None:
        """Remove formatação do CNPJ, retorna apenas dígitos.
        Ex: '12.345.678/0001-90' → '12345678000190'"""
        v = self.texto(valor)
        if not v:
            return None
        return re.sub(r"\D", "", v)

    def limpar_telefone(self, valor) -> str | None:
        """Remove formatação do telefone, retorna apenas dígitos.
        Ex: '(11) 99999-9999' → '11999999999'"""
        v = self.texto(valor)
        if not v:
            return None
        return re.sub(r"\D", "", v)