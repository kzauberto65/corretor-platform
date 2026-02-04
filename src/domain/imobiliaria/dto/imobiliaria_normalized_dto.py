from dataclasses import dataclass

@dataclass
class ImobiliariaNormalizedDTO:
    nome: str | None
    cnpj: str | None
    contato: str | None
    observacoes: str | None
