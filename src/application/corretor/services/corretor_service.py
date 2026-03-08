# ============================================================
# SERVICE: CorretorService
# Camada: application/corretor/services/
# Descrição: Orquestra operações de negócio para Corretores.
#            Recebe InputDTO, normaliza via Normalizer, persiste
#            via Repository e retorna DTO de leitura.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

from typing import Optional, List
from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO
from src.domain.corretor.dto.corretor_dto import CorretorDTO
from src.domain.corretor.entities.corretor_entity import CorretorEntity
from src.application.corretor.normalizers.corretor_normalizer import CorretorNormalizer
from src.infrastructure.corretor.repositories.corretor_repository import CorretorRepository


class CorretorService:

    def __init__(self, repo: Optional[CorretorRepository] = None):
        # Injeção de dependência opcional para facilitar testes mockados
        self.repo = repo or CorretorRepository()

    # ----------------------------------------------------------
    # CONVERSÃO ENTITY → DTO (exigido pela arquitetura)
    # ----------------------------------------------------------

    def _entity_to_dto(self, entity: CorretorEntity) -> CorretorDTO:
        """Converte uma CorretorEntity em CorretorDTO de leitura."""
        return CorretorDTO(
            id=entity.id,
            nome=entity.nome,
            telefone=entity.telefone,
            email=entity.email,
            creci=entity.creci,
            observacoes=entity.observacoes
        )

    # ----------------------------------------------------------
    # OPERAÇÕES DE NEGÓCIO
    # ----------------------------------------------------------

    def cadastrar(self, dto: CorretorInputDTO) -> CorretorDTO:
        """Cadastra um novo corretor após aplicar normalização e validação."""
        if not dto.nome or dto.nome.strip() == "":
            raise ValueError("Nome do corretor é obrigatório")

        normalized = CorretorNormalizer.normalize(dto)
        
        # Cria Entity (sem ID, pois será gerado pelo BD)
        entity = CorretorEntity(
            nome=normalized.nome,
            telefone=normalized.telefone,
            email=normalized.email,
            creci=normalized.creci,
            observacoes=normalized.observacoes
        )
        
        # Delega ao Repository padronizado (que usa .save)
        saved = self.repo.save(entity)
        return self._entity_to_dto(saved)

    def atualizar(self, corretor_id: int, dto: CorretorInputDTO) -> CorretorDTO:
        """Atualiza os dados de um corretor já existente."""
        entity = self.repo.find_by_id(corretor_id)
        if not entity:
            raise ValueError("Corretor não encontrado")

        if not dto.nome or dto.nome.strip() == "":
            raise ValueError("Nome do corretor é obrigatório")

        normalized = CorretorNormalizer.normalize(dto)
        
        # Atualiza a entidade existente
        entity.nome = normalized.nome
        entity.telefone = normalized.telefone
        entity.email = normalized.email
        entity.creci = normalized.creci
        entity.observacoes = normalized.observacoes

        updated = self.repo.save(entity)
        return self._entity_to_dto(updated)

    def listar_todos(self) -> List[CorretorDTO]:
        """Recupera todos os corretores ativos."""
        entities = self.repo.find()
        return [self._entity_to_dto(e) for e in entities]

    def buscar_por_id(self, corretor_id: int) -> Optional[CorretorDTO]:
        """Busca um corretor específico usando apenas o ID."""
        entity = self.repo.find_by_id(corretor_id)
        if not entity:
            return None
        return self._entity_to_dto(entity)

    def remover(self, corretor_id: int) -> bool:
        """Remove o corretor pelo ID, validando antes se existe."""
        entity = self.repo.find_by_id(corretor_id)
        if not entity:
            raise ValueError("Corretor não encontrado")
        return self.repo.delete(corretor_id)