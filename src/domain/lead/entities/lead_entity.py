from dataclasses import dataclass

@dataclass
class LeadEntity:
    id: int | None

    # Básico
    nome: str | None
    email: str | None
    telefone: str | None
    origem: str | None

    # Novos campos do banco
    data_ingestao: str | None
    status: str | None

    # Tags
    tags: str | None

    # Perfil imobiliário
    intencao: str | None
    tipo_imovel: str | None
    faixa_preco: str | None
    preco_min: float | None
    preco_max: float | None
    quartos: int | None
    vagas: int | None
    metragem_min: float | None
    metragem_max: float | None
    bairro_interesse: str | None
    regiao_interesse: str | None
    cidade_interesse: str | None
    urgencia: str | None
    motivo: str | None

    # Marketing & Tracking
    utm_source: str | None
    utm_medium: str | None
    utm_campaign: str | None
    utm_term: str | None
    utm_content: str | None
    canal_preferido: str | None

    # Dados ricos
    profile_json: str | None
    historico_json: str | None

    # Score
    score_lead: float | None

    # Auditoria
    criado_em: str | None
    atualizado_em: str | None
