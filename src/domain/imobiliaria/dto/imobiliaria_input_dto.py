from dataclasses import dataclass

@dataclass
class ImobiliariaInputDTO:
    nome: str | None
    cnpj: str | None
    contato: str | None
    observacoes: str | None
