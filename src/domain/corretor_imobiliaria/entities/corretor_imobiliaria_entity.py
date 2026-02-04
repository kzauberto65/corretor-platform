from dataclasses import dataclass

@dataclass
class CorretorImobiliariaEntity:
    corretor_id: int
    imobiliaria_id: int
    tipo_vinculo: str | None
    observacoes: str | None
