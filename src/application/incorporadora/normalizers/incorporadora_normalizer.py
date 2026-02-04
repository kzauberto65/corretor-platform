from src.domain.incorporadora.dto.incorporadora_input_dto import IncorporadoraInputDTO
from src.domain.incorporadora.dto.incorporadora_normalized_dto import IncorporadoraNormalizedDTO

class IncorporadoraNormalizer:

    @staticmethod
    def normalize(dto: IncorporadoraInputDTO) -> IncorporadoraNormalizedDTO:
        def clean(value):
            if value is None:
                return None
            if isinstance(value, str):
                value = value.strip()
                return value if value != "" else None
            return value

        return IncorporadoraNormalizedDTO(
            nome=clean(dto.nome),
            cnpj=clean(dto.cnpj),
            reputacao=clean(dto.reputacao),
            historico_obra=clean(dto.historico_obra)
        )
