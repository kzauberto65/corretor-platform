from dataclasses import dataclass

@dataclass
class CorretorUnidadeNormalizedDTO:
    corretor_id: int
    unidade_id: int
    tipo_vinculo: str | None
    observacoes: str | None
