from src.domain.spe.dto.spe_input_dto import SPEInputDTO
from src.domain.spe.dto.spe_dto import SPEDTO
from src.domain.spe.entities.spe_entity import SPEEntity
from src.application.spe.normalizers.spe_normalizer import SPENormalizer
from src.infrastructure.spe.repositories.spe_repository import SPERepository

class SPEService:

    def __init__(self, repository: SPERepository):
        self.repository = repository

    def cadastrar(self, dto: SPEInputDTO) -> SPEDTO:
        normalized = SPENormalizer.normalize(dto)
        entity = SPEEntity(
            id=None,
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            observacoes=normalized.observacoes
        )
        created = self.repository.cadastrar(entity)
        return SPEDTO(**created.__dict__)

    def atualizar(self, id: int, dto: SPEInputDTO) -> SPEDTO:
        normalized = SPENormalizer.normalize(dto)
        entity = SPEEntity(
            id=id,
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            observacoes=normalized.observacoes
        )
        updated = self.repository.atualizar(entity)
        return SPEDTO(**updated.__dict__)

    def consultar(self) -> list[SPEDTO]:
        lista = self.repository.consultar()
        return [SPEDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> SPEDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return SPEDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
