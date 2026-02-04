from dataclasses import dataclass

@dataclass
class EmpreendimentoFilterDTO:
    nome: str | None = None
    cidade: str | None = None
    estado: str | None = None
    tipo: str | None = None
    tipologia: str | None = None
