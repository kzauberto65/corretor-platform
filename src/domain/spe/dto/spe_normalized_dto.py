from dataclasses import dataclass

@dataclass
class SPENormalizedDTO:
    nome: str | None
    cnpj: str | None
    observacoes: str | None
