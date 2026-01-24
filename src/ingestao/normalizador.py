import re
from datetime import datetime
import unicodedata


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

        v = v.replace("R$", "").replace(" ", "")
        v = v.replace(".", "").replace(",", ".")

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

    # -------------------------
    # CONSULTAS / BUSCA
    # -------------------------

    def texto_busca(self, valor):
        """
        Normaliza texto para consultas:
        - remove acentos
        - converte para minúsculas
        - remove espaços extras
        """
        v = self.texto(valor)
        if not v:
            return None

        v = unicodedata.normalize("NFD", v)
        v = "".join(c for c in v if unicodedata.category(c) != "Mn")
        return v.lower()
