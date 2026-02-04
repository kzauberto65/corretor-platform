from dataclasses import dataclass

@dataclass
class SPEDTO:
    id: int | None
    nome: str | None
    cnpj: str | None
    observacoes: str | None
