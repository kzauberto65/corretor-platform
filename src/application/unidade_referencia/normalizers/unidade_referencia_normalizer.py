from src.domain.unidade_referencia.dto.unidade_referencia_input_dto import UnidadeReferenciaInputDTO
from src.domain.unidade_referencia.dto.unidade_referencia_normalized_dto import UnidadeReferenciaNormalizedDTO

class UnidadeReferenciaNormalizer:

    @staticmethod
    def normalize(dto: UnidadeReferenciaInputDTO) -> UnidadeReferenciaNormalizedDTO:
        def clean(value: str) -> str:
            value = value.strip()
            return value

        return UnidadeReferenciaNormalizedDTO(
            codigo=clean(dto.codigo)
        )
