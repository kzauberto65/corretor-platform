from dataclasses import dataclass

@dataclass
class IncorporadoraImobiliariaNormalizedDTO:
    incorporadora_id: int
    imobiliaria_id: int
    observacoes: str | None = None
