from dataclasses import dataclass

@dataclass
class ConstrutoraImobiliariaInputDTO:
    construtora_id: int
    imobiliaria_id: int
    tipo_parceria: str | None
    observacoes: str | None
