"""
Enumeração para os Perfis de Comprador aceitos no financiamento.
"""
from enum import Enum

class PerfilCompradorEnum(str, Enum):
    HIS = "HIS"
    HMP = "HMP"
    R2V = "R2V"
    OUTROS = "Outros"