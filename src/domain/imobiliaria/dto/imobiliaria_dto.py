from dataclasses import dataclass

@dataclass
class ImobiliariaDTO:
    id: int | None
    nome: str | None
    cnpj: str | None
    contato: str | None
    observacoes: str | None
