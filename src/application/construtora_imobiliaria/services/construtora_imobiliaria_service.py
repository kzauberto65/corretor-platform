from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_input_dto import ConstrutoraImobiliariaInputDTO
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_dto import ConstrutoraImobiliariaDTO
from src.domain.construtora_imobiliaria.entities.construtora_imobiliaria_entity import ConstrutoraImobiliariaEntity
from src.domain.construtora_imobiliaria.normalizers.construtora_imobiliaria_normalizer import ConstrutoraImobiliariaNormalizer
from src.infrastructure.construtora_imobiliaria.repositories.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository


class ConstrutoraImobiliariaService:

    def __init__(self, repository: ConstrutoraImobiliariaRepository):
        self.repository = repository

    def cadastrar(self, dto: ConstrutoraImobiliariaInputDTO) -> ConstrutoraImobiliariaDTO:
        normalized = ConstrutoraImobiliariaNormalizer.normalize(dto)

        entity = ConstrutoraImobiliariaEntity(
            construtora_id=normalized.construtora_id,
            imobiliaria_id=normalized.imobiliaria_id,
            tipo_parceria=normalized.tipo_parceria,
            observacoes=normalized.observacoes
        )

        created = self.repository.cadastrar(entity)

        return ConstrutoraImobiliariaDTO(
            construtora_id=created.construtora_id,
            imobiliaria_id=created.imobiliaria_id,
            tipo_parceria=created.tipo_parceria,
            observacoes=created.observacoes
        )

    def atualizar(self, dto: ConstrutoraImobiliariaInputDTO) -> ConstrutoraImobiliariaDTO:
        normalized = ConstrutoraImobiliariaNormalizer.normalize(dto)

        entity = ConstrutoraImobiliariaEntity(
            construtora_id=normalized.construtora_id,
            imobiliaria_id=normalized.imobiliaria_id,
            tipo_parceria=normalized.tipo_parceria,
            observacoes=normalized.observacoes
        )

        updated = self.repository.atualizar(entity)

        return ConstrutoraImobiliariaDTO(
            construtora_id=updated.construtora_id,
            imobiliaria_id=updated.imobiliaria_id,
            tipo_parceria=updated.tipo_parceria,
            observacoes=updated.observacoes
        )

    def consultar(self) -> list[ConstrutoraImobiliariaDTO]:
        return self.repository.consultar()

    def buscar_por_ids(self, construtora_id: int, imobiliaria_id: int) -> ConstrutoraImobiliariaDTO | None:
        return self.repository.buscar_por_ids(construtora_id, imobiliaria_id)

    def remover(self, construtora_id: int, imobiliaria_id: int) -> bool:
        return self.repository.remover(construtora_id, imobiliaria_id)
