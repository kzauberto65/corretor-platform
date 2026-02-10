import unicodedata

class LeadNormalizer:

    @staticmethod
    def _clean_str(value):
        if value is None:
            return None
        value = str(value).strip().lower()
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        return value if value else None

    @staticmethod
    def _to_float(value, default=None):
        try:
            if value is None:
                return default
            return float(str(value).replace(",", "."))
        except:
            return default

    @staticmethod
    def _to_int(value, default=None):
        try:
            if value is None:
                return default
            return int(value)
        except:
            return default

    @staticmethod
    def normalize(dto) -> dict:
        """
        Aceita tanto LeadInputDTO quanto LeadEntity do banco.
        Retorna um dicionário normalizado pronto para o MatchingEngine.
        """

        return {
            "id": getattr(dto, "id", None),

            # Strings normalizadas
            "nome": LeadNormalizer._clean_str(getattr(dto, "nome", None)),
            "email": LeadNormalizer._clean_str(getattr(dto, "email", None)),
            "telefone": LeadNormalizer._clean_str(getattr(dto, "telefone", None)),
            "origem": LeadNormalizer._clean_str(getattr(dto, "origem", None)),
            "tags": LeadNormalizer._clean_str(getattr(dto, "tags", None)),

            # Perfil imobiliário
            "intencao": LeadNormalizer._clean_str(getattr(dto, "intencao", None)),
            "tipo_imovel": LeadNormalizer._clean_str(getattr(dto, "tipo_imovel", None)),

            "preco_min": LeadNormalizer._to_float(getattr(dto, "preco_min", None), 0.0),
            "preco_max": LeadNormalizer._to_float(getattr(dto, "preco_max", None), 999999999.0),

            "quartos": LeadNormalizer._to_int(getattr(dto, "quartos", None)),
            "vagas": LeadNormalizer._to_int(getattr(dto, "vagas", None)),

            "metragem_min": LeadNormalizer._to_float(getattr(dto, "metragem_min", None)),
            "metragem_max": LeadNormalizer._to_float(getattr(dto, "metragem_max", None)),

            "bairro_interesse": LeadNormalizer._clean_str(getattr(dto, "bairro_interesse", None)),
            "regiao_interesse": LeadNormalizer._clean_str(getattr(dto, "regiao_interesse", None)),
            "cidade_interesse": LeadNormalizer._clean_str(getattr(dto, "cidade_interesse", None)),

            "urgencia": LeadNormalizer._clean_str(getattr(dto, "urgencia", None)),
            "motivo": LeadNormalizer._clean_str(getattr(dto, "motivo", None)),
        }
