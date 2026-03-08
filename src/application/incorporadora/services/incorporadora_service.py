# ============================================================
# SERVICE: IncorporadoraService
# Camada: application/incorporadora/services/
# Descrição: Orquestra operações de negócio para Incorporadora.
#            Aplica normalização de dados e persiste via Repository.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

from typing import Optional, List

from src.domain.incorporadora.dto.incorporadora_input_dto import IncorporadoraInputDTO
from src.domain.incorporadora.dto.incorporadora_dto import IncorporadoraDTO
from src.domain.incorporadora.entities.incorporadora_entity import IncorporadoraEntity
from src.application.incorporadora.normalizers.incorporadora_normalizer import IncorporadoraNormalizer
from src.infrastructure.incorporadora.repositories.incorporadora_repository import IncorporadoraRepository


class IncorporadoraService:

    def __init__(self, repository: Optional[IncorporadoraRepository] = None):
        self.repository = repository or IncorporadoraRepository()

    # ----------------------------------------------------------
    # CONVERSÃO ENTITY → DTO (Exigido pela arquitetura)
    # ----------------------------------------------------------
    def _entity_to_dto(self, entity: IncorporadoraEntity) -> IncorporadoraDTO:
        """Converte uma IncorporadoraEntity em IncorporadoraDTO com segurança."""
        return IncorporadoraDTO(
            id=entity.id,
            nome=entity.nome,
            cnpj=entity.cnpj,
            reputacao=entity.reputacao,
            historico_obra=entity.historico_obra
        )

    # ----------------------------------------------------------
    # OPERAÇÕES DE NEGÓCIO
    # ----------------------------------------------------------
    def cadastrar(self, dto: IncorporadoraInputDTO) -> IncorporadoraDTO:
        """Cadastra uma nova incorporadora após normalização."""
        normalized = IncorporadoraNormalizer.normalize(dto)
        
        if not normalized.nome or not normalized.nome.strip():
            raise ValueError("O nome da incorporadora é obrigatório.")

        # Cria a entidade sem ID (será gerado pelo repositório)
        entity = IncorporadoraEntity(
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            reputacao=normalized.reputacao,
            historico_obra=normalized.historico_obra
        )
        
        saved_entity = self.repository.save(entity)
        return self._entity_to_dto(saved_entity)

    def atualizar(self, incorporadora_id: int, dto: IncorporadoraInputDTO) -> IncorporadoraDTO:
        """Atualiza os dados de uma incorporadora existente."""
        entity = self.repository.find_by_id(incorporadora_id)
        if not entity:
            raise ValueError("Incorporadora não encontrada.")

        normalized = IncorporadoraNormalizer.normalize(dto)
        
        if not normalized.nome or not normalized.nome.strip():
            raise ValueError("O nome da incorporadora é obrigatório.")

        # Atualiza apenas os campos mutáveis da entidade localizada
        entity.nome = normalized.nome
        entity.cnpj = normalized.cnpj
        entity.reputacao = normalized.reputacao
        entity.historico_obra = normalized.historico_obra

        updated_entity = self.repository.save(entity)
        return self._entity_to_dto(updated_entity)

    def listar(self) -> List[IncorporadoraDTO]:
        """Retorna todas as incorporadoras cadastradas."""
        entities = self.repository.find()
        return [self._entity_to_dto(entity) for entity in entities]

    def buscar_por_id(self, incorporadora_id: int) -> Optional[IncorporadoraDTO]:
        """Busca incorporadora específica pelo ID."""
        entity = self.repository.find_by_id(incorporadora_id)
        if not entity:
            return None
        return self._entity_to_dto(entity)

    def remover(self, incorporadora_id: int) -> bool:
        """Remove a incorporadora após validar sua existência."""
        entity = self.repository.find_by_id(incorporadora_id)
        if not entity:
            raise ValueError("Incorporadora não encontrada.")
            
        return self.repository.delete(incorporadora_id)