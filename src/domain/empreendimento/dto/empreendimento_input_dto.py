# ============================================================
# DTO: EmpreendimentoInputDTO
# Camada: domain/empreendimento/dto/
# Descrição: Dados de entrada para criação de um empreendimento.
#            Empreendimento é contexto institucional — não contém
#            mais preco, tipologia, metragem_min/max (Sprint 10.5).
#            Esses dados agora vivem em cada unidade individualmente.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class EmpreendimentoInputDTO:
    # Identificação principal
    nome: Optional[str]                 # nome comercial do empreendimento

    # Localização
    regiao: Optional[str]               # ex: Zona Sul, Grande ABC
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]               # sigla: SP, RJ, MG...
    endereco: Optional[str]             # endereço completo

    # Caracterização do produto
    produto: Optional[str]              # ex: residencial vertical, comercial, loteamento
    tipo: Optional[str]                 # ex: apartamento, casa, studio
    descricao: Optional[str]            # descrição comercial do empreendimento

    # Cronograma
    periodo_lancamento: Optional[str]   # ex: Q1/2025
    data_entrega: Optional[str]         # formato ISO: YYYY-MM-DD
    status_entrega: Optional[str]       # ex: em obras / pronto / entregue

    # Atributos do produto (contexto institucional)
    total_unidades: Optional[int]       # total de unidades do empreendimento
    amenities: Optional[str]            # JSON com lista de amenidades
                                        # ex: '["piscina", "academia", "salão de festas"]'
    padrao_construtivo: Optional[str]   # JSON com padrão construtivo
                                        # ex: '{"acabamento": "alto", "construtora": "A"}'

    # Relacionamentos institucionais
    incorporadora_id: Optional[int]     # FK → incorporadora(id)
    proprietario_id: Optional[int]      # FK → construtoras(id)
    spe_id: Optional[int]               # FK → spe(id)
    unidade_referencia_id: Optional[int] # FK → unidades(id) — unidade padrão do empreendimento

    # CAMPOS REMOVIDOS NA SPRINT 10.5 — NÃO REINTRODUZIR:
    # preco         → agora em unidades.preco
    # tipologia     → agora em unidades.tipo_unidade
    # metragem_min  → agora em unidades.metragem
    # metragem_max  → agora em unidades.metragem