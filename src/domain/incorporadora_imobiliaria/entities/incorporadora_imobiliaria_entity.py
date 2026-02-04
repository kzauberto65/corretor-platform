from dataclasses import dataclass

@dataclass
class IncorporadoraImobiliariaEntity:
    incorporadora_id: int
    imobiliaria_id: int
    observacoes: str | None = None
