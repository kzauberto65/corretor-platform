from src.domain.spe.dto.spe_input_dto import SPEInputDTO
from src.domain.spe.dto.spe_normalized_dto import SPENormalizedDTO

class SPENormalizer:

    @staticmethod
    def normalize(dto: SPEInputDTO) -> SPENormalizedDTO:
        def clean(value):
            if value is None:
                return None
            if isinstance(value, str):
                value = value.strip()
                return value if value != "" else None
            return value

        return SPENormalizedDTO(
            nome=clean(dto.nome),
            cnpj=clean(dto.cnpj),
            observacoes=clean(dto.observacoes)
        )
