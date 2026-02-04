from src.domain.unidade_referencia_tipo.dto.unidade_referencia_tipo_input_dto import UnidadeReferenciaTipoInputDTO
from src.domain.unidade_referencia_tipo.dto.unidade_referencia_tipo_normalized_dto import UnidadeReferenciaTipoNormalizedDTO

class UnidadeReferenciaTipoNormalizer:

    @staticmethod
    def normalize(dto: UnidadeReferenciaTipoInputDTO) -> UnidadeReferenciaTipoNormalizedDTO:
        def clean(value: str) -> str:
            value = value.strip()
            return value

        return UnidadeReferenciaTipoNormalizedDTO(
            nome=clean(dto.nome)
        )
