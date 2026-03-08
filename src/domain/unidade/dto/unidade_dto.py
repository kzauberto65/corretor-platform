# ============================================================
# DTO: UnidadeDTO
# Camada: domain/unidade/dto/
# Descrição: Representação completa de uma unidade já persistida.
#            Inclui id e created_at — usado para leitura e exibição.
#            Retornado pelo Repository após consultas ao banco.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class UnidadeDTO:
    # Identificador do banco — None apenas antes de persistir
    id: Optional[int]

    # Vínculo com o empreendimento
    empreendimento_id: int

    # Identificação da unidade
    codigo_unidade: Optional[str]       # ex: AP-101, GARDEN-02, COB-PH

    # Atributos comerciais principais
    preco: Optional[float]              # preço de venda em R$
    metragem: Optional[float]           # área privativa em m²
    dormitorios: Optional[int]          # número de dormitórios
    suites: Optional[int]               # número de suítes
    vagas: Optional[int]                # vagas de garagem

    # Tipologia e localização interna
    tipo_unidade: Optional[str]         # studio / 1dorm / 2dorm / garden / cobertura / casa
    andar: Optional[int]                # andar (0 = térreo)

    # Status comercial
    disponibilidade: Optional[str]      # disponível / vendido / reservado

    # Descrição e notas
    descricao_unidade: Optional[str]    # descrição comercial da unidade
    observacoes: Optional[str]          # notas internas

    # Auditoria
    created_at: Optional[str]           # datetime ISO gerado automaticamente pelo banco