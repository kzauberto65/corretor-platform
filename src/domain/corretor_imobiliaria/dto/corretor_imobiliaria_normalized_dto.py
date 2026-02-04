from dataclasses import dataclass

@dataclass
class CorretorImobiliariaNormalizedDTO:
    corretor_id: int
    imobiliaria_id: int
    tipo_vinculo: str | None
    observacoes: str | None
