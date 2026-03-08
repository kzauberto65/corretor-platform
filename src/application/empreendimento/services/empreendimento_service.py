# ============================================================
# SERVICE: EmpreendimentoService
# Camada: application/empreendimento/services/
# Descrição: Orquestra operações de empreendimento.
#            Recebe InputDTO → Normalizer → Entity → Repository.
#            Zero acesso direto ao banco — papel do Repository.
#            Zero lógica de apresentação — papel da CLI/API.
# ATENÇÃO API FUTURA: service já preparado para ser chamado
#            por controller FastAPI sem modificações.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.empreendimento.dto.empreendimento_dto import EmpreendimentoDTO
from src.domain.empreendimento.entities.empreendimento_entity import EmpreendimentoEntity
from src.application.empreendimento.normalizers.empreendimento_normalizer import EmpreendimentoNormalizer


class EmpreendimentoService:

    def __init__(self, repo):
        # Repository injetado — facilita testes unitários com mock
        self.repo = repo

    # ----------------------------------------------------------
    # HELPERS PRIVADOS
    # ----------------------------------------------------------

    def _normalized_to_entity(self, empreendimento_id, normalized) -> EmpreendimentoEntity:
        """Monta EmpreendimentoEntity a partir do NormalizedDTO.
        id=None para criação, id=valor para atualização."""
        return EmpreendimentoEntity(
            id=empreendimento_id,
            nome=normalized.nome,
            regiao=normalized.regiao,
            bairro=normalized.bairro,
            cidade=normalized.cidade,
            estado=normalized.estado,
            endereco=normalized.endereco,
            produto=normalized.produto,
            tipo=normalized.tipo,
            descricao=normalized.descricao,
            periodo_lancamento=normalized.periodo_lancamento,
            data_entrega=normalized.data_entrega,
            status_entrega=normalized.status_entrega,
            total_unidades=normalized.total_unidades,
            amenities=normalized.amenities,
            padrao_construtivo=normalized.padrao_construtivo,
            incorporadora_id=normalized.incorporadora_id,
            proprietario_id=normalized.proprietario_id,
            spe_id=normalized.spe_id,
            unidade_referencia_id=normalized.unidade_referencia_id
        )

    def _entity_to_dto(self, entity: EmpreendimentoEntity) -> EmpreendimentoDTO:
        """Converte EmpreendimentoEntity para EmpreendimentoDTO.
        Mapeamento explícito — mais seguro que **__dict__."""
        return EmpreendimentoDTO(
            id=entity.id,
            nome=entity.nome,
            regiao=entity.regiao,
            bairro=entity.bairro,
            cidade=entity.cidade,
            estado=entity.estado,
            endereco=entity.endereco,
            produto=entity.produto,
            tipo=entity.tipo,
            descricao=entity.descricao,
            periodo_lancamento=entity.periodo_lancamento,
            data_entrega=entity.data_entrega,
            status_entrega=entity.status_entrega,
            total_unidades=entity.total_unidades,
            amenities=entity.amenities,
            padrao_construtivo=entity.padrao_construtivo,
            incorporadora_id=entity.incorporadora_id,
            proprietario_id=entity.proprietario_id,
            spe_id=entity.spe_id,
            unidade_referencia_id=entity.unidade_referencia_id
        )

    # ----------------------------------------------------------
    # ESCRITA
    # ----------------------------------------------------------

    def cadastrar(self, input_dto: EmpreendimentoInputDTO) -> EmpreendimentoDTO:
        """Normaliza, persiste e retorna o empreendimento criado.
        Fluxo: InputDTO → Normalizer → Entity → Repository → DTO"""
        normalized = EmpreendimentoNormalizer.normalize(input_dto)
        entity = self._normalized_to_entity(None, normalized)
        saved = self.repo.save(entity)
        return self._entity_to_dto(saved)

    def atualizar(self, empreendimento_id: int, input_dto: EmpreendimentoInputDTO) -> EmpreendimentoDTO | None:
        """Atualiza um empreendimento existente.
        Verifica existência antes de atualizar.
        Retorna None se não encontrado."""
        existente = self.repo.find_by_id(empreendimento_id)
        if not existente:
            return None

        normalized = EmpreendimentoNormalizer.normalize(input_dto)
        entity = self._normalized_to_entity(empreendimento_id, normalized)
        updated = self.repo.update(entity)
        return self._entity_to_dto(updated)

    def remover(self, empreendimento_id: int) -> bool:
        """Remove um empreendimento pelo id.
        Retorna False se não encontrado.
        ATENÇÃO: falhará se houver unidades vinculadas (FK constraint)."""
        existente = self.repo.find_by_id(empreendimento_id)
        if not existente:
            return False
        self.repo.delete(empreendimento_id)
        return True

    # ----------------------------------------------------------
    # LEITURA
    # ----------------------------------------------------------

    def listar_todos(self) -> list[EmpreendimentoDTO]:
        """Retorna todos os empreendimentos cadastrados."""
        return [self._entity_to_dto(e) for e in self.repo.find()]

    def buscar_por_id(self, empreendimento_id: int) -> EmpreendimentoDTO | None:
        """Busca empreendimento pelo id. Retorna None se não encontrado."""
        entity = self.repo.find_by_id(empreendimento_id)
        return self._entity_to_dto(entity) if entity else None

    def consultar(
        self,
        cidade=None,
        regiao=None,
        status_entrega=None,
        periodo_lancamento=None,
        incorporadora_id=None,
        ordenar_por=None,
        ordem="asc"
    ) -> list[EmpreendimentoDTO]:
        """Consulta empreendimentos com filtros opcionais.

        FILTROS DISPONÍVEIS (pós-Sprint 10.5):
          cidade, regiao, status_entrega, periodo_lancamento, incorporadora_id

        FILTROS REMOVIDOS (não existem mais em empreendimentos):
          preco_min/max → usar UnidadeService.listar_disponiveis() e filtrar
          metragem_min/max → idem
        """
        entities = self.repo.find_filtered(
            cidade=cidade,
            regiao=regiao,
            status_entrega=status_entrega,
            periodo_lancamento=periodo_lancamento,
            incorporadora_id=incorporadora_id,
            ordenar_por=ordenar_por,
            ordem=ordem
        )
        return [self._entity_to_dto(e) for e in entities]

    def listar_com_unidades_disponiveis(self) -> list[EmpreendimentoDTO]:
        """Retorna apenas empreendimentos que têm unidades disponíveis.
        Usado pelo pipeline de Offer e Matching para não processar
        empreendimentos esgotados."""
        entities = self.repo.find_disponiveis()
        return [self._entity_to_dto(e) for e in entities]

    def listar_por_incorporadora(self, incorporadora_id: int) -> list[EmpreendimentoDTO]:
        """Retorna todos os empreendimentos de uma incorporadora.
        Útil para relatórios e dashboards por incorporadora."""
        entities = self.repo.find_by_incorporadora(incorporadora_id)
        return [self._entity_to_dto(e) for e in entities]