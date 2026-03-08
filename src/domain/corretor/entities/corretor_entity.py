from dataclasses import dataclass

@dataclass
class CorretorEntity:
    id: int | None = None  # <-- Adicionar o valor default aqui
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None
    creci: str | None = None
    observacoes: str | None = None