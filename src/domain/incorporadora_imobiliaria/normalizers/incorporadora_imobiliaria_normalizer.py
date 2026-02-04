from src.domain.incorporadora_imobiliaria.dto.incorporadora_imobiliaria_input_dto import IncorporadoraImobiliariaInputDTO
from src.domain.incorporadora_imobiliaria.dto.incorporadora_imobiliaria_normalized_dto import IncorporadoraImobiliariaNormalizedDTO

class IncorporadoraImobiliariaNormalizer:

    @staticmethod
    def normalize(dto: IncorporadoraImobiliariaInputDTO) -> IncorporadoraImobiliariaNormalizedDTO:
        return IncorporadoraImobiliariaNormalizedDTO(
            incorporadora_id=int(dto.incorporadora_id),
            imobiliaria_id=int(dto.imobiliaria_id),
            observacoes=dto.observacoes.strip() if dto.observacoes else None
        )
