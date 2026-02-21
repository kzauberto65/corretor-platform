from dataclasses import dataclass

@dataclass
class LeadDTO:
    id: int | None = None

    # Básico
    nome: str | None = None
    email: str | None = None
    telefone: str | None = None
    origem: str | None = None

    # Novos campos do banco
    data_ingestao: str | None = None
    status: str | None = None

    # Tags
    tags: str | None = None

    # Perfil imobiliário
    intencao: str | None = None
    tipo_imovel: str | None = None
    faixa_preco: str | None = None
    preco_min: float | None = None
    preco_max: float | None = None
    quartos: int | None = None
    vagas: int | None = None
    metragem_min: float | None = None
    metragem_max: float | None = None
    bairro_interesse: str | None = None
    regiao_interesse: str | None = None
    cidade_interesse: str | None = None
    urgencia: str | None = None
    motivo: str | None = None

    # Marketing & Tracking
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_term: str | None = None
    utm_content: str | None = None
    canal_preferido: str | None = None

    # Dados ricos
    profile_json: str | None = None
    historico_json: str | None = None

    # Score
    score_lead: float | None = None

    # Auditoria
    criado_em: str | None = None
    atualizado_em: str | None = None
