from src.domain.unidade_referencia_tipo.dto.unidade_referencia_tipo_input_dto import UnidadeReferenciaTipoInputDTO
from src.domain.unidade_referencia_tipo.dto.unidade_referencia_tipo_dto import UnidadeReferenciaTipoDTO
from src.domain.unidade_referencia_tipo.entities.unidade_referencia_tipo_entity import UnidadeReferenciaTipoEntity
from src.application.unidade_referencia_tipo.normalizers.unidade_referencia_tipo_normalizer import UnidadeReferenciaTipoNormalizer
from src.infrastructure.unidade_referencia_tipo.repositories.unidade_referencia_tipo_repository import UnidadeReferenciaTipoRepository

class UnidadeReferenciaTipoService:

    def __init__(self, repository: UnidadeReferenciaTipoRepository):
        self.repository = repository

    def cadastrar(self, dto: UnidadeReferenciaTipoInputDTO) -> UnidadeReferenciaTipoDTO:
        normalized = UnidadeReferenciaTipoNormalizer.normalize(dto)
        entity = UnidadeReferenciaTipoEntity(
            id=None,
            nome=normalized.nome
        )
        created = self.repository.cadastrar(entity)
        return UnidadeReferenciaTipoDTO(**created.__dict__)

    def atualizar(self, id: int, dto: UnidadeReferenciaTipoInputDTO) -> UnidadeReferenciaTipoDTO:
        normalized = UnidadeReferenciaTipoNormalizer.normalize(dto)
        entity = UnidadeReferenciaTipoEntity(
            id=id,
            nome=normalized.nome
        )
        updated = self.repository.atualizar(entity)
        return UnidadeReferenciaTipoDTO(**updated.__dict__)

    def consultar(self) -> list[UnidadeReferenciaTipoDTO]:
        lista = self.repository.consultar()
        return [UnidadeReferenciaTipoDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> UnidadeReferenciaTipoDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return UnidadeReferenciaTipoDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
