from dataclasses import dataclass

@dataclass
class CorretorImobiliariaInputDTO:
    corretor_id: int
    imobiliaria_id: int
    tipo_vinculo: str | None
    observacoes: str | None
