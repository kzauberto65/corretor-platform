"""
Enumeração para as Condições de Uso da unidade.
"""
from enum import Enum

class CondicaoUsoEnum(str, Enum):
    MORADIA_PROPRIA = "moradia_propria"
    ALUGUEL_CURTA_DURACAO = "aluguel_curta_duracao"
    OUTROS = "Outros"