from dataclasses import dataclass

@dataclass
class IncorporadoraInputDTO:
    nome: str | None
    cnpj: str | None
    reputacao: int | None
    historico_obra: str | None
