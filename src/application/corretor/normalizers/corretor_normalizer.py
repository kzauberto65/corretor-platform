from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO
from src.domain.corretor.dto.corretor_normalized_dto import CorretorNormalizedDTO

class CorretorNormalizer:

    @staticmethod
    def normalize(dto: CorretorInputDTO) -> CorretorNormalizedDTO:
        def clean(value: str | None) -> str | None:
            if value is None:
                return None
            value = value.strip()
            return value if value != "" else None

        return CorretorNormalizedDTO(
            nome=clean(dto.nome),
            telefone=clean(dto.telefone),
            email=clean(dto.email),
            creci=clean(dto.creci),
            observacoes=clean(dto.observacoes)
        )
