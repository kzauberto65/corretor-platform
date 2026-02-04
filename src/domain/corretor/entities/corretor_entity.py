from dataclasses import dataclass

@dataclass
class CorretorEntity:
    id: int | None
    nome: str | None
    telefone: str | None
    email: str | None
    creci: str | None
    observacoes: str | None
