from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_input_dto import ConstrutoraImobiliariaInputDTO
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_normalized_dto import ConstrutoraImobiliariaNormalizedDTO

class ConstrutoraImobiliariaNormalizer:

    @staticmethod
    def normalize(dto: ConstrutoraImobiliariaInputDTO) -> ConstrutoraImobiliariaNormalizedDTO:
        return ConstrutoraImobiliariaNormalizedDTO(
            construtora_id=int(dto.construtora_id),
            imobiliaria_id=int(dto.imobiliaria_id),
            tipo_parceria=dto.tipo_parceria.strip() if dto.tipo_parceria else None,
            observacoes=dto.observacoes.strip() if dto.observacoes else None
        )
