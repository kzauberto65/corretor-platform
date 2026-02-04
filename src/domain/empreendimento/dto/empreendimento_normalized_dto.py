from dataclasses import dataclass

@dataclass
class EmpreendimentoNormalizedDTO:
    regiao: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None
    produto: str | None
    endereco: str | None
    data_entrega: str | None
    status_entrega: str | None
    tipo: str | None
    descricao: str | None
    preco: float | None
    proprietario_id: int | None
    incorporadora_id: int | None
    unidade_referencia_id: int | None
    spe_id: int | None
    periodo_lancamento: str | None
    nome: str | None
    tipologia: str | None
