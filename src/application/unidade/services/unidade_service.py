from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO
from src.domain.unidade.dto.unidade_dto import UnidadeDTO
from src.domain.unidade.entities.unidade_entity import UnidadeEntity
from src.application.unidade.normalizers.unidade_normalizer import UnidadeNormalizer
from src.infrastructure.unidade.repositories.unidade_repository import UnidadeRepository

class UnidadeService:

    def __init__(self, repository: UnidadeRepository):
        self.repository = repository

    def cadastrar(self, dto: UnidadeInputDTO) -> UnidadeDTO:
        normalized = UnidadeNormalizer.normalize(dto)
        entity = UnidadeEntity(
            id=None,
            empreendimento_id=normalized.empreendimento_id,
            construtora_id=normalized.construtora_id,
            codigo_unidade=normalized.codigo_unidade,
            metragem=normalized.metragem,
            valor=normalized.valor,
            observacoes=normalized.observacoes,
            tipo_unidade_id=normalized.tipo_unidade_id
        )
        created = self.repository.cadastrar(entity)
        return UnidadeDTO(**created.__dict__)

    def atualizar(self, id: int, dto: UnidadeInputDTO) -> UnidadeDTO:
        normalized = UnidadeNormalizer.normalize(dto)
        entity = UnidadeEntity(
            id=id,
            empreendimento_id=normalized.empreendimento_id,
            construtora_id=normalized.construtora_id,
            codigo_unidade=normalized.codigo_unidade,
            metragem=normalized.metragem,
            valor=normalized.valor,
            observacoes=normalized.observacoes,
            tipo_unidade_id=normalized.tipo_unidade_id
        )
        updated = self.repository.atualizar(entity)
        return UnidadeDTO(**updated.__dict__)

    def consultar(self) -> list[UnidadeDTO]:
        lista = self.repository.consultar()
        return [UnidadeDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> UnidadeDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return UnidadeDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
