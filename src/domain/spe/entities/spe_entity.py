from dataclasses import dataclass

@dataclass
class SPEEntity:
    id: int | None
    nome: str | None
    cnpj: str | None
    observacoes: str | None
