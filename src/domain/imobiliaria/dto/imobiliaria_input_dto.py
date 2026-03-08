# ============================================================
# DTO: ImobiliariaInputDTO
# Camada: domain/imobiliaria/dto/
# Descrição: Input DTO para criação/atualização de Imobiliária
# Sprint: 10.5
# ============================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class ImobiliariaInputDTO:
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    contato: Optional[str] = None
    observacoes: Optional[str] = None