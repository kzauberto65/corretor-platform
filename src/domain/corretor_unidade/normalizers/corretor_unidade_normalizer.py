from src.domain.corretor_unidade.dto.corretor_unidade_input_dto import CorretorUnidadeInputDTO
from src.domain.corretor_unidade.dto.corretor_unidade_normalized_dto import CorretorUnidadeNormalizedDTO

class CorretorUnidadeNormalizer:

    @staticmethod
    def normalize(dto: CorretorUnidadeInputDTO) -> CorretorUnidadeNormalizedDTO:
        return CorretorUnidadeNormalizedDTO(
            corretor_id=int(dto.corretor_id),
            unidade_id=int(dto.unidade_id),
            tipo_vinculo=dto.tipo_vinculo.strip() if dto.tipo_vinculo else None,
            observacoes=dto.observacoes.strip() if dto.observacoes else None
        )
