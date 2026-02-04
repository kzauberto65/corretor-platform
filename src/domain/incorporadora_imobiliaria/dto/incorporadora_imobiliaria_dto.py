from dataclasses import dataclass

@dataclass
class IncorporadoraImobiliariaDTO:
    incorporadora_id: int
    imobiliaria_id: int
    observacoes: str | None = None
