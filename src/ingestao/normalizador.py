# src/ingestao/normalizador.py

import re
from datetime import datetime

class Normalizador:

    # -------------------------
    # TEXTOS
    # -------------------------

    def texto(self, valor):
        if valor is None:
            return None
        v = str(valor).strip()
        if v.lower() in ("nan", "none", ""):
            return None
        return v

    def texto_titulo(self, valor):
        v = self.texto(valor)
        return v.title() if v else None

    # -------------------------
    # NÚMEROS
    # -------------------------

    def numero(self, valor):
        v = self.texto(valor)
        return v if v else None

    def inteiro(self, valor):
        v = self.texto(valor)
        if not v:
            return None
        try:
            return int(float(v.replace(",", ".")))
        except:
            return None

    def flutuante(self, valor):
        v = self.texto(valor)
        if not v:
            return None

        # Trata formatos tipo "24,69" ou "24.69"
        v = v.replace(",", ".")
        try:
            return float(v)
        except:
            return None

    # -------------------------
    # MOEDA
    # -------------------------

    def moeda(self, valor):
        v = self.texto(valor)
        if not v:
            return None

        # Remove símbolos e formatações
        v = v.replace("R$", "").replace(" ", "")
        v = v.replace(".", "").replace(",", ".")  # 650.000,00 → 650000.00

        try:
            return float(v)
        except:
            return None

    # -------------------------
    # DATAS
    # -------------------------

    def data(self, valor):
        v = self.texto(valor)
        if not v:
            return None

        formatos = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%d/%m/%y",
        ]

        for fmt in formatos:
            try:
                return datetime.strptime(v, fmt).date().isoformat()
            except:
                pass

        # Se não reconheceu, retorna texto original
        return v

    # -------------------------
    # DOCUMENTOS
    # -------------------------

    def limpar_cnpj(self, valor):
        v = self.texto(valor)
        if not v:
            return None
        return re.sub(r"\D", "", v)

    def limpar_telefone(self, valor):
        v = self.texto(valor)
        if not v:
            return None
        return re.sub(r"\D", "", v)