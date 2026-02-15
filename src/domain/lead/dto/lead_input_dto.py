from dataclasses import dataclass

@dataclass
class LeadInputDTO:
    # Básico
    nome: str | None = None
    email: str | None = None
    telefone: str | None = None
    origem: str | None = None
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
    cidade_interesse: str | None = None
    urgencia: str | None = None
    motivo: str | None = None
    regiao_interesse: str | None = None

    # Marketing & Tracking
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_term: str | None = None
    utm_content: str | None = None
    canal_preferido: str | None = None

    # Dados ricos
    dados_completos: dict | None = None
