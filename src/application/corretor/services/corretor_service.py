from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO
from src.domain.corretor.dto.corretor_dto import CorretorDTO
from src.domain.corretor.entities.corretor_entity import CorretorEntity
from src.application.corretor.normalizers.corretor_normalizer import CorretorNormalizer
from src.infrastructure.corretor.repositories.corretor_repository import CorretorRepository

class CorretorService:

    def __init__(self, repository: CorretorRepository):
        self.repository = repository

    def cadastrar(self, dto: CorretorInputDTO) -> CorretorDTO:
        normalized = CorretorNormalizer.normalize(dto)
        entity = CorretorEntity(
            id=None,
            nome=normalized.nome,
            telefone=normalized.telefone,
            email=normalized.email,
            creci=normalized.creci,
            observacoes=normalized.observacoes
        )
        created = self.repository.cadastrar(entity)
        return CorretorDTO(**created.__dict__)

    def atualizar(self, id: int, dto: CorretorInputDTO) -> CorretorDTO:
        normalized = CorretorNormalizer.normalize(dto)
        entity = CorretorEntity(
            id=id,
            nome=normalized.nome,
            telefone=normalized.telefone,
            email=normalized.email,
            creci=normalized.creci,
            observacoes=normalized.observacoes
        )
        updated = self.repository.atualizar(entity)
        return CorretorDTO(**updated.__dict__)

    def consultar(self) -> list[CorretorDTO]:
        lista = self.repository.consultar()
        return [CorretorDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> CorretorDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return CorretorDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
