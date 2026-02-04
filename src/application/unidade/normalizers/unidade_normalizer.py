from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO
from src.domain.unidade.dto.unidade_normalized_dto import UnidadeNormalizedDTO

class UnidadeNormalizer:

    @staticmethod
    def normalize(dto: UnidadeInputDTO) -> UnidadeNormalizedDTO:
        return UnidadeNormalizedDTO(
            empreendimento_id=dto.empreendimento_id,
            construtora_id=dto.construtora_id,
            codigo_unidade=dto.codigo_unidade.strip() if dto.codigo_unidade else None,
            metragem=dto.metragem,
            valor=dto.valor,
            observacoes=dto.observacoes.strip() if dto.observacoes else None,
            tipo_unidade_id=dto.tipo_unidade_id
        )
