from src.domain.incorporadora.dto.incorporadora_input_dto import IncorporadoraInputDTO
from src.domain.incorporadora.dto.incorporadora_dto import IncorporadoraDTO
from src.domain.incorporadora.entities.incorporadora_entity import IncorporadoraEntity
from src.application.incorporadora.normalizers.incorporadora_normalizer import IncorporadoraNormalizer
from src.infrastructure.incorporadora.repositories.incorporadora_repository import IncorporadoraRepository

class IncorporadoraService:

    def __init__(self, repository: IncorporadoraRepository):
        self.repository = repository

    def cadastrar(self, dto: IncorporadoraInputDTO) -> IncorporadoraDTO:
        normalized = IncorporadoraNormalizer.normalize(dto)
        entity = IncorporadoraEntity(
            id=None,
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            reputacao=normalized.reputacao,
            historico_obra=normalized.historico_obra
        )
        created = self.repository.cadastrar(entity)
        return IncorporadoraDTO(**created.__dict__)

    def atualizar(self, id: int, dto: IncorporadoraInputDTO) -> IncorporadoraDTO:
        normalized = IncorporadoraNormalizer.normalize(dto)
        entity = IncorporadoraEntity(
            id=id,
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            reputacao=normalized.reputacao,
            historico_obra=normalized.historico_obra
        )
        updated = self.repository.atualizar(entity)
        return IncorporadoraDTO(**updated.__dict__)

    def consultar(self) -> list[IncorporadoraDTO]:
        lista = self.repository.consultar()
        return [IncorporadoraDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> IncorporadoraDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return IncorporadoraDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
