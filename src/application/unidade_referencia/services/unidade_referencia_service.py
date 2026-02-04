from src.domain.unidade_referencia.dto.unidade_referencia_input_dto import UnidadeReferenciaInputDTO
from src.domain.unidade_referencia.dto.unidade_referencia_dto import UnidadeReferenciaDTO
from src.domain.unidade_referencia.entities.unidade_referencia_entity import UnidadeReferenciaEntity
from src.application.unidade_referencia.normalizers.unidade_referencia_normalizer import UnidadeReferenciaNormalizer
from src.infrastructure.unidade_referencia.repositories.unidade_referencia_repository import UnidadeReferenciaRepository

class UnidadeReferenciaService:

    def __init__(self, repository: UnidadeReferenciaRepository):
        self.repository = repository

    def criar_ou_obter(self, codigo: str) -> UnidadeReferenciaDTO:
        existente = self.repository.buscar_por_codigo(codigo)
        if existente:
            return UnidadeReferenciaDTO(**existente.__dict__)

        dto = UnidadeReferenciaInputDTO(codigo=codigo)
        return self.cadastrar(dto)

    def cadastrar(self, dto: UnidadeReferenciaInputDTO) -> UnidadeReferenciaDTO:
        normalized = UnidadeReferenciaNormalizer.normalize(dto)
        entity = UnidadeReferenciaEntity(
            id=None,
            codigo=normalized.codigo
        )
        created = self.repository.cadastrar(entity)
        return UnidadeReferenciaDTO(**created.__dict__)

    def atualizar(self, id: int, dto: UnidadeReferenciaInputDTO) -> UnidadeReferenciaDTO:
        normalized = UnidadeReferenciaNormalizer.normalize(dto)
        entity = UnidadeReferenciaEntity(
            id=id,
            codigo=normalized.codigo
        )
        updated = self.repository.atualizar(entity)
        return UnidadeReferenciaDTO(**updated.__dict__)

    def consultar(self) -> list[UnidadeReferenciaDTO]:
        lista = self.repository.consultar()
        return [UnidadeReferenciaDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> UnidadeReferenciaDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return UnidadeReferenciaDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
