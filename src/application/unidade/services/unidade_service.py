# ============================================================
# SERVICE: UnidadeService
# Camada: application/unidade/services/
# Descrição: Orquestra as operações de unidade.
#            Recebe DTOs, chama Normalizer, monta Entity,
#            delega ao Repository e retorna DTOs de saída.
#            Zero acesso direto ao banco — isso é papel do Repository.
#            Zero lógica de apresentação — isso é papel da CLI/API.
# ATENÇÃO API FUTURA: este service já está preparado para ser chamado
#            por um controller FastAPI sem qualquer modificação.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO
from src.domain.unidade.dto.unidade_dto import UnidadeDTO
from src.domain.unidade.entities.unidade_entity import UnidadeEntity
from src.application.unidade.normalizers.unidade_normalizer import UnidadeNormalizer
from src.infrastructure.unidade.repositories.unidade_repository import UnidadeRepository


class UnidadeService:

    def __init__(self, repository: UnidadeRepository):
        # Repository injetado — facilita testes unitários com mock
        self.repository = repository

    # ----------------------------------------------------------
    # HELPERS PRIVADOS
    # ----------------------------------------------------------

    def _entity_to_dto(self, entity: UnidadeEntity) -> UnidadeDTO:
        """Converte UnidadeEntity para UnidadeDTO.
        Centralizado aqui para não repetir em cada método.
        Evita uso de **__dict__ que é frágil a mudanças de campos."""
        return UnidadeDTO(
            id=entity.id,
            empreendimento_id=entity.empreendimento_id,
            codigo_unidade=entity.codigo_unidade,
            preco=entity.preco,
            metragem=entity.metragem,
            dormitorios=entity.dormitorios,
            suites=entity.suites,
            vagas=entity.vagas,
            tipo_unidade=entity.tipo_unidade,
            andar=entity.andar,
            disponibilidade=entity.disponibilidade,
            descricao_unidade=entity.descricao_unidade,
            observacoes=entity.observacoes,
            created_at=entity.created_at
        )

    def _normalized_to_entity(self, unidade_id: int | None, normalized) -> UnidadeEntity:
        """Monta UnidadeEntity a partir do NormalizedDTO.
        Recebe id=None para criação, id=valor para atualização."""
        return UnidadeEntity(
            id=unidade_id,
            empreendimento_id=normalized.empreendimento_id,
            codigo_unidade=normalized.codigo_unidade,
            preco=normalized.preco,
            metragem=normalized.metragem,
            dormitorios=normalized.dormitorios,
            suites=normalized.suites,
            vagas=normalized.vagas,
            tipo_unidade=normalized.tipo_unidade,
            andar=normalized.andar,
            disponibilidade=normalized.disponibilidade,
            descricao_unidade=normalized.descricao_unidade,
            observacoes=normalized.observacoes,
            created_at=None  # gerado automaticamente pelo banco
        )

    # ----------------------------------------------------------
    # ESCRITA
    # ----------------------------------------------------------

    def cadastrar(self, dto: UnidadeInputDTO) -> UnidadeDTO:
        """Normaliza, persiste e retorna a unidade criada.
        Fluxo: InputDTO → Normalizer → Entity → Repository → DTO"""
        normalized = UnidadeNormalizer.normalize(dto)
        entity = self._normalized_to_entity(None, normalized)
        created = self.repository.cadastrar(entity)
        return self._entity_to_dto(created)

    def atualizar(self, unidade_id: int, dto: UnidadeInputDTO) -> UnidadeDTO | None:
        """Atualiza uma unidade existente.
        Verifica se a unidade existe antes de atualizar.
        Retorna None se não encontrada."""
        # Verificar existência antes de atualizar
        existente = self.repository.buscar_por_id(unidade_id)
        if not existente:
            return None

        normalized = UnidadeNormalizer.normalize(dto)
        entity = self._normalized_to_entity(unidade_id, normalized)
        updated = self.repository.atualizar(entity)
        return self._entity_to_dto(updated)

    def atualizar_disponibilidade(self, unidade_id: int, disponibilidade: str) -> bool:
        """Atualiza apenas o status de disponibilidade.
        Usado para marcar unidade como vendida ou reservada rapidamente.
        Valores aceitos: disponível / vendido / reservado"""
        return self.repository.atualizar_disponibilidade(unidade_id, disponibilidade)

    def remover(self, unidade_id: int) -> bool:
        """Remove uma unidade pelo id.
        Verifica existência antes de tentar remover."""
        existente = self.repository.buscar_por_id(unidade_id)
        if not existente:
            return False
        return self.repository.remover(unidade_id)

    # ----------------------------------------------------------
    # LEITURA
    # ----------------------------------------------------------

    def consultar(self) -> list[UnidadeDTO]:
        """Retorna todas as unidades cadastradas.
        Para uso em CLI e relatórios administrativos."""
        return [self._entity_to_dto(e) for e in self.repository.consultar()]

    def buscar_por_id(self, unidade_id: int) -> UnidadeDTO | None:
        """Busca uma unidade pelo id.
        Retorna None se não encontrada."""
        entity = self.repository.buscar_por_id(unidade_id)
        return self._entity_to_dto(entity) if entity else None

    def listar_por_empreendimento(self, empreendimento_id: int) -> list[UnidadeDTO]:
        """Retorna todas as unidades de um empreendimento.
        Inclui vendidas e reservadas — para visão administrativa."""
        entities = self.repository.list_by_empreendimento(empreendimento_id)
        return [self._entity_to_dto(e) for e in entities]

    def listar_disponiveis(self) -> list[UnidadeDTO]:
        """Retorna apenas unidades disponíveis para venda.
        Usado pelo pipeline de Matching e IA."""
        entities = self.repository.list_disponiveis()
        return [self._entity_to_dto(e) for e in entities]

    def listar_disponiveis_por_empreendimento(self, empreendimento_id: int) -> list[UnidadeDTO]:
        """Retorna unidades disponíveis de um empreendimento específico.
        Usado pelo corretor para ver o que ainda pode ofertar."""
        entities = self.repository.list_disponiveis_by_empreendimento(empreendimento_id)
        return [self._entity_to_dto(e) for e in entities]

    def resumo_empreendimento(self, empreendimento_id: int) -> dict:
        """Retorna contagem de unidades por status de disponibilidade.
        Ex: {"disponível": 5, "vendido": 3, "reservado": 1}
        Útil para dashboard e relatório de empreendimento."""
        return self.repository.contar_by_empreendimento(empreendimento_id)