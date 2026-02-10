from dataclasses import dataclass

@dataclass
class EmpreendimentoNormalizedDTO:
    id: int | None = None
    regiao: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    produto: str | None = None
    endereco: str | None = None
    data_entrega: str | None = None
    status_entrega: str | None = None
    tipo: str | None = None
    descricao: str | None = None
    preco: float | None = None
    proprietario_id: int | None = None
    incorporadora_id: int | None = None
    unidade_referencia_id: int | None = None
    spe_id: int | None = None
    periodo_lancamento: str | None = None
    nome: str | None = None
    tipologia: str | None = None

    # 🔥 CAMPOS NOVOS
    metragem_min: float | None = None
    metragem_max: float | None = None
