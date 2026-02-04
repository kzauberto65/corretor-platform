from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_input_dto import CorretorImobiliariaInputDTO
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_normalized_dto import CorretorImobiliariaNormalizedDTO

class CorretorImobiliariaNormalizer:

    @staticmethod
    def normalize(dto: CorretorImobiliariaInputDTO) -> CorretorImobiliariaNormalizedDTO:
        return CorretorImobiliariaNormalizedDTO(
            corretor_id=int(dto.corretor_id),
            imobiliaria_id=int(dto.imobiliaria_id),
            tipo_vinculo=dto.tipo_vinculo.strip() if dto.tipo_vinculo else None,
            observacoes=dto.observacoes.strip() if dto.observacoes else None
        )
