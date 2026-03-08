# ============================================================
# DTO: EmpreendimentoDTO
# Camada: domain/empreendimento/dto/
# Descrição: Representação completa de um empreendimento persistido.
#            Inclui id e created_at — usado para leitura e exibição.
#            Retornado pelo Repository após consultas ao banco.
#            Empreendimento = contexto institucional (Sprint 10.5).
#            Dados comerciais (preco, tipologia, metragem) estão em unidades.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EmpreendimentoDTO:
    # Identificador do banco — None apenas antes de persistir
    id: Optional[int] = None

    # Identificação principal
    nome: Optional[str] = None              # nome comercial do empreendimento

    # Localização
    regiao: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None            # sigla: SP, RJ, MG...
    endereco: Optional[str] = None

    # Caracterização do produto
    produto: Optional[str] = None           # ex: residencial vertical, comercial
    tipo: Optional[str] = None              # ex: apartamento, casa, studio
    descricao: Optional[str] = None

    # Cronograma
    periodo_lancamento: Optional[str] = None
    data_entrega: Optional[str] = None      # formato ISO: YYYY-MM-DD
    status_entrega: Optional[str] = None    # em obras / pronto / entregue

    # Atributos institucionais
    total_unidades: Optional[int] = None
    amenities: Optional[str] = None         # JSON com lista de amenidades
    padrao_construtivo: Optional[str] = None # JSON com padrão construtivo

    # Relacionamentos
    incorporadora_id: Optional[int] = None  # FK → incorporadora(id)
    proprietario_id: Optional[int] = None   # FK → construtoras(id)
    spe_id: Optional[int] = None            # FK → spe(id)
    unidade_referencia_id: Optional[int] = None  # FK → unidades(id)

    # CAMPOS REMOVIDOS NA SPRINT 10.5 — NÃO REINTRODUZIR:
    # preco, tipologia, metragem_min, metragem_max → agora em unidades