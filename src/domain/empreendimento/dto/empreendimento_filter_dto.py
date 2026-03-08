# ============================================================
# DTO: EmpreendimentoFilterDTO
# Camada: domain/empreendimento/dto/
# Descrição: Parâmetros de filtro para consulta de empreendimentos.
#            Usado pela CLI e futura API para montar queries no Repository.
#            Todos os campos são opcionais — None = sem filtro.
#
# FILTROS REMOVIDOS NA SPRINT 10.5 — NÃO REINTRODUZIR:
#   metragem_min, metragem_max → agora em unidades
#   preco_min, preco_max       → agora em unidades
#   tipologia                  → agora em unidades.tipo_unidade
#
# Para filtrar por preço ou metragem usar UnidadeFilterDTO.
# ============================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class EmpreendimentoFilterDTO:
    # Identificação
    nome: Optional[str] = None              # busca parcial (LIKE)

    # Localização
    cidade: Optional[str] = None            # busca parcial (LIKE)
    estado: Optional[str] = None            # busca exata (sigla: SP, RJ...)
    regiao: Optional[str] = None            # busca parcial (LIKE)
    bairro: Optional[str] = None            # busca parcial (LIKE)

    # Produto
    tipo: Optional[str] = None              # busca parcial (LIKE)
    produto: Optional[str] = None           # busca parcial (LIKE)

    # Cronograma
    status_entrega: Optional[str] = None    # ex: em obras / pronto / entregue
    periodo_lancamento: Optional[str] = None # busca parcial (LIKE)

    # Relacionamentos
    incorporadora_id: Optional[int] = None  # busca exata

    # Ordenação e paginação
    ordenar_por: Optional[str] = None       # nome / cidade / regiao / entrega / status
    ordem: str = "asc"                      # asc / desc