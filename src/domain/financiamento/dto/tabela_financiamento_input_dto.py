# src/domain/unidade/dto/tabela_financiamento_input_dto.py
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class PerfilComprador(str, Enum):
    HIS = "HIS"
    HMP = "HMP"
    R2V = "R2V"
    OUTROS = "Outros"

class CondicaoUso(str, Enum):
    MORADIA_PROPRIA = "moradia_propria"
    ALUGUEL_CURTA_DURACAO = "aluguel_curta_duracao"
    OUTROS = "outros"

@dataclass
class TabelaFinanciamentoInputDTO:
    unidade_id: int
    perfil_comprador: PerfilComprador
    condicao_uso: CondicaoUso
    
    valor_entrada: float = 0.0
    valor_mensais: float = 0.0
    qtde_mensais: int = 0
    valor_intermediarias: float = 0.0
    qtde_intermediarias: int = 0
    valor_chaves: float = 0.0
    valor_financiamento: float = 0.0
    
    renda_teto_familiar: Optional[float] = None
    renda_minima_exigida: float = 0.0