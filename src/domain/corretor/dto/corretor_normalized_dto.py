from dataclasses import dataclass

@dataclass
class CorretorNormalizedDTO:
    nome: str | None
    telefone: str | None
    email: str | None
    creci: str | None
    observacoes: str | None
