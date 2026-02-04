from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO
from src.domain.construtora.dto.construtora_dto import ConstrutoraDTO
from src.domain.construtora.entities.construtora_entity import ConstrutoraEntity
from src.application.construtora.normalizers.construtora_normalizer import ConstrutoraNormalizer
from src.infrastructure.construtora.repositories.construtora_repository import ConstrutoraRepository

class ConstrutoraService:

    def __init__(self, repository: ConstrutoraRepository):
        self.repository = repository

    def cadastrar(self, dto: ConstrutoraInputDTO) -> ConstrutoraDTO:
        normalized = ConstrutoraNormalizer.normalize(dto)
        entity = ConstrutoraEntity(
            id=None,
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            contato=normalized.contato,
            observacoes=normalized.observacoes,
            fonte=normalized.fonte,
            data_registro=normalized.data_registro,
            usuario_id=normalized.usuario_id,
            justificativa=normalized.justificativa
        )
        created = self.repository.cadastrar(entity)
        return ConstrutoraDTO(**created.__dict__)

    def atualizar(self, id: int, dto: ConstrutoraInputDTO) -> ConstrutoraDTO:
        normalized = ConstrutoraNormalizer.normalize(dto)
        entity = ConstrutoraEntity(
            id=id,
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            contato=normalized.contato,
            observacoes=normalized.observacoes,
            fonte=normalized.fonte,
            data_registro=normalized.data_registro,
            usuario_id=normalized.usuario_id,
            justificativa=normalized.justificativa
        )
        updated = self.repository.atualizar(entity)
        return ConstrutoraDTO(**updated.__dict__)

    def consultar(self) -> list[ConstrutoraDTO]:
        lista = self.repository.consultar()
        return [ConstrutoraDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> ConstrutoraDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return ConstrutoraDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
