from dataclasses import dataclass

@dataclass
class SPEInputDTO:
    nome: str | None
    cnpj: str | None
    observacoes: str | None
