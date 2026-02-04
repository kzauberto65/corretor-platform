from dataclasses import dataclass

@dataclass
class IncorporadoraNormalizedDTO:
    nome: str | None
    cnpj: str | None
    reputacao: int | None
    historico_obra: str | None
