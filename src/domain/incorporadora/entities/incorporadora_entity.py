from dataclasses import dataclass

@dataclass
class IncorporadoraEntity:
    id: int | None
    nome: str | None
    cnpj: str | None
    reputacao: int | None
    historico_obra: str | None
