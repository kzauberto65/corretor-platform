from dataclasses import dataclass

@dataclass
class MailingDTO:
    id: int | None

    # Básico
    nome: str | None
    email: str | None
    telefone: str | None
    origem: str | None
    tags: str | None

    # Datas e ingestão
    data_ingestao: str | None
    fonte_arquivo: str | None

    # Validação
    valido: int | None
    motivo_invalidacao: str | None
    hash_unico: str | None

    # Perfil pessoal
    sexo: str | None
    data_nascimento: str | None
    idade: int | None
    estado_civil: str | None
    nacionalidade: str | None
    profissao: str | None
    empresa: str | None
    cargo: str | None
    renda_mensal: float | None
    faixa_renda: str | None
    escolaridade: str | None

    # Endereço
    cep: str | None
    logradouro: str | None
    numero: str | None
    complemento: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None
    pais: str | None

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
    cidade_interesse: str | None
    urgencia: str | None
    motivo: str | None

    # Marketing & Tracking
    utm_source: str | None
    utm_medium: str | None
    utm_campaign: str | None
    utm_term: str | None
    utm_content: str | None
    primeiro_contato: str | None
    ultimo_contato: str | None
    canal_preferido: str | None
    score_mailing: float | None

    # Auditoria
    criado_em: str | None
    atualizado_em: str | None
