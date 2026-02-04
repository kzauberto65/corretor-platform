from dataclasses import dataclass

@dataclass
class UnidadeDTO:
    id: int | None
    empreendimento_id: int
    construtora_id: int | None
    codigo_unidade: str | None
    metragem: float | None
    valor: float | None
    observacoes: str | None
    tipo_unidade_id: int | None
