"""
Data Transfer Objects (DTOs) para a entidade Tabela Financiamento.
Isolam a entrada e saída de dados da camada de aplicação.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class TabelaFinanciamentoInputDTO:
    unidade_id: int
    perfil_comprador: str
    condicao_uso: str
    valor_entrada: float = 0.0
    valor_mensais: float = 0.0
    qtde_mensais: int = 0
    valor_intermediarias: float = 0.0
    qtde_intermediarias: int = 0
    valor_chaves: float = 0.0
    valor_financiamento: float = 0.0
    renda_minima_exigida: float = 0.0
    renda_teto_familiar: Optional[float] = None

@dataclass
class TabelaFinanciamentoOutputDTO:
    id: int
    unidade_id: int
    perfil_comprador: str
    condicao_uso: str
    valor_entrada: float
    valor_mensais: float
    qtde_mensais: int
    valor_intermediarias: float
    qtde_intermediarias: int
    valor_chaves: float
    valor_financiamento: float
    renda_minima_exigida: float
    renda_teto_familiar: Optional[float]
    created_at: str