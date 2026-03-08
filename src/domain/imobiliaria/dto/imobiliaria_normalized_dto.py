# ============================================================
# DTO: ImobiliariaNormalizedDTO
# Camada: domain/imobiliaria/dto/
# Descrição: DTO normalizado (após validação/normalização)
# Sprint: 10.5
# ============================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class ImobiliariaNormalizedDTO:
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    contato: Optional[str] = None
    observacoes: Optional[str] = None