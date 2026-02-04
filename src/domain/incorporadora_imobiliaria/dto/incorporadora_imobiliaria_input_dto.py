from dataclasses import dataclass

@dataclass
class IncorporadoraImobiliariaInputDTO:
    incorporadora_id: int
    imobiliaria_id: int
    observacoes: str | None = None
