# ============================================================
# SERVICE: ConstrutoraService
# Camada: application/construtora/services/
# Descrição: Orquestra operações de negócio para Construtoras.
#            Recebe InputDTO, normaliza via Normalizer, persiste
#            via Repository e retorna DTO de leitura.
#            Contém validações de negócio (duplicidade, obrigatoriedade).
#            NÃO acessa banco diretamente — delega ao Repository.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

from typing import Optional, List
from src.infrastructure.construtora.repositories.construtora_repository import ConstrutoraRepository
from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO
from src.domain.construtora.dto.construtora_dto import ConstrutoraDTO
from src.domain.construtora.entities.construtora_entity import ConstrutoraEntity
from src.application.construtora.normalizers.construtora_normalizer import ConstrutoraNormalizer


class ConstrutoraService:

    def __init__(self, repo: Optional[ConstrutoraRepository] = None):
        self.repo = repo or ConstrutoraRepository()

    # ----------------------------------------------------------
    # CONVERSÃO ENTITY → DTO (exigido pela arquitetura)
    # ----------------------------------------------------------

    def _entity_to_dto(self, entity: ConstrutoraEntity) -> ConstrutoraDTO:
        """Converte uma ConstrutoraEntity em ConstrutoraDTO de leitura.
        Centraliza a conversão — se o DTO mudar, só muda aqui."""
        return ConstrutoraDTO(
            id=entity.id,
            nome=entity.nome,
            cnpj=entity.cnpj,
            contato=entity.contato,
            observacoes=entity.observacoes,
            fonte=entity.fonte,
            data_registro=entity.data_registro,
            usuario_id=entity.usuario_id,
            justificativa=entity.justificativa
        )

    # ----------------------------------------------------------
    # OPERAÇÕES DE NEGÓCIO
    # ----------------------------------------------------------

    def cadastrar(self, input_dto: ConstrutoraInputDTO) -> ConstrutoraDTO:
        """Cria uma nova construtora a partir de um InputDTO.
        Fluxo: InputDTO → Normalizer → Entity → Repository → DTO"""

        if not input_dto.nome or input_dto.nome.strip() == "":
            raise ValueError("Nome da construtora é obrigatório")

        existentes = self.repo.find()
        for e in existentes:
            if e.nome and e.nome.strip().lower() == input_dto.nome.strip().lower():
                return self._entity_to_dto(e)

        if input_dto.cnpj:
            for e in existentes:
                if e.cnpj and e.cnpj == input_dto.cnpj:
                    return self._entity_to_dto(e)

        normalized = ConstrutoraNormalizer.normalize(input_dto)

        entity = ConstrutoraEntity(
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            contato=normalized.contato,
            observacoes=normalized.observacoes,
            fonte=normalized.fonte,
            data_registro=normalized.data_registro,
            usuario_id=normalized.usuario_id,
            justificativa=normalized.justificativa
        )

        saved = self.repo.save(entity)
        return self._entity_to_dto(saved)

    def listar_todos(self) -> List[ConstrutoraDTO]:
        """Lista todas as construtoras cadastradas."""
        entities = self.repo.find()
        return [self._entity_to_dto(e) for e in entities]

    def buscar_por_id(self, construtora_id: int) -> Optional[ConstrutoraDTO]:
        """Busca uma construtora pelo ID."""
        entity = self.repo.find_by_id(construtora_id)
        if not entity:
            return None
        return self._entity_to_dto(entity)

    def atualizar(self, construtora_id: int, input_dto: ConstrutoraInputDTO) -> ConstrutoraDTO:
        """Atualiza uma construtora existente."""
        entity = self.repo.find_by_id(construtora_id)
        if not entity:
            raise ValueError("Construtora não encontrada")

        if not input_dto.nome or input_dto.nome.strip() == "":
            raise ValueError("Nome da construtora é obrigatório")

        normalized = ConstrutoraNormalizer.normalize(input_dto)

        entity.nome = normalized.nome
        entity.cnpj = normalized.cnpj
        entity.contato = normalized.contato
        entity.observacoes = normalized.observacoes
        entity.fonte = normalized.fonte
        entity.data_registro = normalized.data_registro
        entity.usuario_id = normalized.usuario_id
        entity.justificativa = normalized.justificativa

        updated = self.repo.save(entity)
        return self._entity_to_dto(updated)

    def remover(self, construtora_id: int) -> bool:
        """Remove uma construtora pelo ID."""
        entity = self.repo.find_by_id(construtora_id)
        if not entity:
            raise ValueError("Construtora não encontrada")
        return self.repo.delete(construtora_id)