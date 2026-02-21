import re
import unicodedata
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.empreendimento.dto.empreendimento_normalized_dto import EmpreendimentoNormalizedDTO


class EmpreendimentoNormalizer:

    @staticmethod
    def _clean_str(value):
        if not value:
            return None
        value = value.strip().lower()
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        return value if value else None

    @staticmethod
    def _extract_metragem(value):
        if not value:
            return None, None

        value = value.replace(",", ".").lower()
        match = re.findall(r"(\d+\.?\d*)", value)

        if len(match) >= 2:
            return float(match[0]), float(match[1])

        return None, None

    @staticmethod
    def _normalize_tipo(tipo):
        if not tipo:
            return None

        tipo = EmpreendimentoNormalizer._clean_str(tipo)

        mapping = {
            "apartamento": "apartamento",
            "casa": "casa",
            "studio": "studio",
            "cobertura": "cobertura",
        }

        for key in mapping:
            if key in tipo:
                return mapping[key]

        return tipo

    @staticmethod
    def normalize(input_dto) -> EmpreendimentoNormalizedDTO:
        """
        Funciona tanto para:
        - EmpreendimentoInputDTO (ingestão)
        - EmpreendimentoDTO (banco → Offer Engine)
        """

        # 🔵 Se o DTO tiver id, preserva. Se não tiver, vira None.
        id_value = getattr(input_dto, "id", None)

        cidade = EmpreendimentoNormalizer._clean_str(input_dto.cidade)
        bairro = EmpreendimentoNormalizer._clean_str(input_dto.bairro)
        regiao = EmpreendimentoNormalizer._clean_str(input_dto.regiao)
        tipo = EmpreendimentoNormalizer._normalize_tipo(input_dto.tipo)
        tipologia = EmpreendimentoNormalizer._clean_str(input_dto.tipologia)

        metragem_min, metragem_max = EmpreendimentoNormalizer._extract_metragem(
            input_dto.tipologia or ""
        )

        return EmpreendimentoNormalizedDTO(
            id=id_value,
            regiao=regiao,
            bairro=bairro,
            cidade=cidade,
            estado=EmpreendimentoNormalizer._clean_str(input_dto.estado),
            produto=EmpreendimentoNormalizer._clean_str(input_dto.produto),
            endereco=EmpreendimentoNormalizer._clean_str(input_dto.endereco),
            data_entrega=input_dto.data_entrega,
            status_entrega=EmpreendimentoNormalizer._clean_str(input_dto.status_entrega),
            tipo=tipo,
            descricao=EmpreendimentoNormalizer._clean_str(input_dto.descricao),
            preco=input_dto.preco,
            proprietario_id=input_dto.proprietario_id,
            incorporadora_id=input_dto.incorporadora_id,
            unidade_referencia_id=input_dto.unidade_referencia_id,
            spe_id=input_dto.spe_id,
            periodo_lancamento=EmpreendimentoNormalizer._clean_str(input_dto.periodo_lancamento),
            nome=EmpreendimentoNormalizer._clean_str(input_dto.nome),
            tipologia=tipologia,
            metragem_min=metragem_min,
            metragem_max=metragem_max,
        )
