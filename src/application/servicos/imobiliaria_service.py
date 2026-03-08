# ============================================================
# SERVICE: ImobiliariaService
# Camada: application/imobiliaria/services/
# Descrição: Orquestra operações de negócio para Imobiliária.
#            Aplica regras de não-duplicidade (nome/CNPJ), 
#            normaliza dados e persiste via Repository.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

from typing import Optional, List

from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO
from src.domain.imobiliaria.dto.imobiliaria_dto import ImobiliariaDTO
from src.domain.imobiliaria.entities.imobiliaria_entity import ImobiliariaEntity
from src.application.imobiliaria.normalizers.imobiliaria_normalizer import ImobiliariaNormalizer
from src.infrastructure.imobiliaria.repositories.imobiliaria_repository import ImobiliariaRepository


class ImobiliariaService:

    def __init__(self, repo: Optional[ImobiliariaRepository] = None):
        self.repo = repo or ImobiliariaRepository()

    # ----------------------------------------------------------
    # CONVERSÃO ENTITY → DTO (Exigido pela arquitetura)
    # ----------------------------------------------------------
    def _entity_to_dto(self, entity: ImobiliariaEntity) -> ImobiliariaDTO:
        """Converte uma ImobiliariaEntity em ImobiliariaDTO de leitura."""
        return ImobiliariaDTO(
            id=entity.id,
            nome=entity.nome,
            cnpj=entity.cnpj,
            contato=entity.contato,
            observacoes=entity.observacoes
        )

    # ----------------------------------------------------------
    # OPERAÇÕES DE NEGÓCIO
    # ----------------------------------------------------------
    def cadastrar(self, dto: ImobiliariaInputDTO) -> ImobiliariaDTO:
        """
        Cadastra uma nova imobiliária garantindo que não existam 
        duplicidades pelo Nome ou pelo CNPJ.
        """
        if not dto.nome or dto.nome.strip() == "":
            raise ValueError("Nome da imobiliária é obrigatório")

        normalized = ImobiliariaNormalizer.normalize(dto)
        
        # Validar duplicidade verificando registros existentes
        # (Idealmente isso seria feito com queries específicas no bd para alta escala)
        existentes = self.repo.find()
        for im in existentes:
            # Evitar duplicidade por nome (case insensitive)
            if im.nome.lower() == normalized.nome.lower():
                return self._entity_to_dto(im)
            
            # Evitar duplicidade por CNPJ (quando informado)
            if normalized.cnpj and im.cnpj == normalized.cnpj:
                return self._entity_to_dto(im)

        # Criar ImobiliariaEntity sem ID (será gerado pelo banco)
        entity = ImobiliariaEntity(
            nome=normalized.nome,
            cnpj=normalized.cnpj,
            contato=normalized.contato,
            observacoes=normalized.observacoes
        )
        
        saved = self.repo.save(entity)
        return self._entity_to_dto(saved)

    def atualizar(self, imobiliaria_id: int, dto: ImobiliariaInputDTO) -> ImobiliariaDTO:
        """Atualiza os dados de uma imobiliária existente."""
        entity = self.repo.find_by_id(imobiliaria_id)
        if not entity:
            raise ValueError("Imobiliária não encontrada")

        if not dto.nome or dto.nome.strip() == "":
            raise ValueError("Nome da imobiliária é obrigatório")

        normalized = ImobiliariaNormalizer.normalize(dto)

        # Verifica duplicidade de CNPJ para outra imobiliária
        if normalized.cnpj:
            existentes = self.repo.find()
            for im in existentes:
                if im.id != imobiliaria_id and im.cnpj == normalized.cnpj:
                    raise ValueError("Já existe outra imobiliária com este CNPJ")

        # Atualiza a entidade existente
        entity.nome = normalized.nome
        entity.cnpj = normalized.cnpj
        entity.contato = normalized.contato
        entity.observacoes = normalized.observacoes

        updated = self.repo.save(entity)
        return self._entity_to_dto(updated)

    def listar(self) -> List[ImobiliariaDTO]:
        """Retorna todas as imobiliárias."""
        entities = self.repo.find()
        return [self._entity_to_dto(e) for e in entities]

    def buscar_por_id(self, imobiliaria_id: int) -> Optional[ImobiliariaDTO]:
        """Busca imobiliária específica pelo ID."""
        entity = self.repo.find_by_id(imobiliaria_id)
        if not entity:
            return None
        return self._entity_to_dto(entity)

    def remover(self, imobiliaria_id: int) -> bool:
        """Remove a imobiliária após validar sua existência."""
        entity = self.repo.find_by_id(imobiliaria_id)
        if not entity:
            raise ValueError("Imobiliária não encontrada")

        return self.repo.delete(imobiliaria_id)