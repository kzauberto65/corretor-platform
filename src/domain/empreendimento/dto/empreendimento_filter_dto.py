from dataclasses import dataclass

@dataclass
class EmpreendimentoFilterDTO:
    nome: str | None = None
    cidade: str | None = None
    estado: str | None = None
    tipo: str | None = None
    metragem_min: float | None = None
    metragem_max: float | None = None
