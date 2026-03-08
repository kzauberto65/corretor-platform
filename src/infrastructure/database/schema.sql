-- ============================================================
-- SCHEMA OFICIAL — CORRETOR PLATFORM
-- Gerado em: 2026 | Sprint 10.5
-- Source of Truth: corretor.db (raiz do projeto)
-- ATENÇÃO: Este arquivo deve estar sempre sincronizado com o banco real.
-- Para recriar o banco do zero: sqlite3 corretor.db < schema.sql
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- BLOCO 1: ENTIDADES BASE (sem dependências externas)
-- Ordem de criação obrigatória — FKs dependem desta ordem
-- ============================================================

-- ------------------------------------------------------------
-- TABELA: construtoras
-- Empresas construtoras vinculadas a empreendimentos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS construtoras (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    cnpj            TEXT,
    contato         TEXT,
    observacoes     TEXT,
    fonte           TEXT,           -- origem do cadastro (planilha, manual, etc.)
    data_registro   TEXT,           -- data de entrada no sistema
    usuario_id      TEXT,           -- usuário que cadastrou
    justificativa   TEXT            -- motivo do cadastro
);

-- ------------------------------------------------------------
-- TABELA: imobiliarias
-- Imobiliárias parceiras ou proprietárias de carteira
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS imobiliarias (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    cnpj        TEXT,
    contato     TEXT,
    observacoes TEXT
);

-- ------------------------------------------------------------
-- TABELA: corretores
-- Corretores vinculados a imobiliárias e unidades
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS corretores (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    telefone    TEXT,
    email       TEXT,
    creci       TEXT,               -- registro profissional obrigatório
    observacoes TEXT
);

-- ------------------------------------------------------------
-- TABELA: incorporadora
-- Incorporadoras responsáveis pelos empreendimentos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS incorporadora (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    cnpj            TEXT,
    reputacao       INTEGER,        -- score interno de reputação (1-5)
    historico_obra  TEXT            -- histórico de obras entregues
);

-- ------------------------------------------------------------
-- TABELA: spe
-- Sociedade de Propósito Específico — entidade jurídica do empreendimento
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS spe (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT,
    cnpj        TEXT,
    observacoes TEXT
);

-- ============================================================
-- BLOCO 2: RELACIONAMENTOS N:N ENTRE ENTIDADES BASE
-- ============================================================

-- ------------------------------------------------------------
-- RELACIONAMENTO: construtoras ↔ imobiliarias
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS construtora_imobiliaria (
    construtora_id  INTEGER NOT NULL,
    imobiliaria_id  INTEGER NOT NULL,
    tipo_parceria   TEXT,           -- ex: exclusiva, preferencial, aberta
    observacoes     TEXT,
    PRIMARY KEY (construtora_id, imobiliaria_id),
    FOREIGN KEY (construtora_id) REFERENCES construtoras(id),
    FOREIGN KEY (imobiliaria_id) REFERENCES imobiliarias(id)
);

-- ------------------------------------------------------------
-- RELACIONAMENTO: corretores ↔ imobiliarias
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS corretor_imobiliaria (
    corretor_id     INTEGER NOT NULL,
    imobiliaria_id  INTEGER NOT NULL,
    tipo_vinculo    TEXT,           -- ex: CLT, autônomo, parceiro
    observacoes     TEXT,
    PRIMARY KEY (corretor_id, imobiliaria_id),
    FOREIGN KEY (corretor_id)     REFERENCES corretores(id),
    FOREIGN KEY (imobiliaria_id)  REFERENCES imobiliarias(id)
);

-- ------------------------------------------------------------
-- RELACIONAMENTO: incorporadora ↔ imobiliarias
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS incorporadora_imobiliaria (
    incorporadora_id    INTEGER NOT NULL,
    imobiliaria_id      INTEGER NOT NULL,
    observacoes         TEXT,
    PRIMARY KEY (incorporadora_id, imobiliaria_id),
    FOREIGN KEY (incorporadora_id)  REFERENCES incorporadora(id),
    FOREIGN KEY (imobiliaria_id)    REFERENCES imobiliarias(id)
);

-- ============================================================
-- BLOCO 3: EMPREENDIMENTOS E UNIDADES
-- Núcleo do modelo de imóveis — Sprint 10.5
-- Empreendimento = contexto institucional
-- Unidade = entidade comercializável real
-- ============================================================

-- ------------------------------------------------------------
-- TABELA: empreendimentos
-- Contexto institucional do produto imobiliário.
-- NÃO contém mais preco, tipologia, metragem_min/max —
-- esses dados agora estão em cada unidade individualmente.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS empreendimentos (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                    TEXT,
    regiao                  TEXT,
    bairro                  TEXT,
    cidade                  TEXT,
    estado                  TEXT,
    produto                 TEXT,       -- ex: residencial vertical, horizontal, comercial
    endereco                TEXT,
    data_entrega            TEXT,       -- formato ISO: YYYY-MM-DD
    status_entrega          TEXT,       -- ex: em obras, pronto, entregue
    tipo                    TEXT,       -- ex: apartamento, casa, studio
    descricao               TEXT,
    periodo_lancamento      TEXT,       -- ex: Q1/2025
    amenities               TEXT,       -- JSON com lista de amenidades
    padrao_construtivo      TEXT,       -- JSON com padrão construtivo
    total_unidades          INTEGER,    -- total de unidades do empreendimento

    -- Relacionamentos institucionais
    incorporadora_id        INTEGER,    -- incorporadora responsável
    proprietario_id         INTEGER,    -- construtora proprietária
    spe_id                  INTEGER,    -- SPE vinculada
    unidade_referencia_id   INTEGER,    -- unidade padrão para referência comercial

    FOREIGN KEY (incorporadora_id)      REFERENCES incorporadora(id),
    FOREIGN KEY (proprietario_id)       REFERENCES construtoras(id),
    FOREIGN KEY (spe_id)                REFERENCES spe(id),
    FOREIGN KEY (unidade_referencia_id) REFERENCES unidades(id)  -- definida abaixo
);

-- ------------------------------------------------------------
-- TABELA: unidades
-- Entidade comercializável real — cada linha é um imóvel vendável.
-- Vinculada ao empreendimento como contexto.
-- É aqui que IA e Matching operam.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS unidades (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendimento_id   INTEGER NOT NULL,   -- empreendimento ao qual pertence
    codigo_unidade      TEXT,               -- ex: AP-101, GARDEN-02
    preco               REAL,               -- preço atual de venda
    metragem            REAL,               -- área privativa em m²
    dormitorios         INTEGER,            -- número de dormitórios
    suites              INTEGER,            -- número de suítes
    vagas               INTEGER,            -- vagas de garagem
    tipo_unidade        TEXT,               -- studio / 1dorm / 2dorm / garden / cobertura / casa
    andar               INTEGER,            -- andar (0 = térreo)
    disponibilidade     TEXT,               -- disponível / vendido / reservado
    descricao_unidade   TEXT,               -- descrição comercial da unidade
    observacoes         TEXT,               -- notas internas
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (empreendimento_id) REFERENCES empreendimentos(id)
);

-- ------------------------------------------------------------
-- TABELA: unidade_referencia
-- Unidade padrão de referência comercial do empreendimento.
-- Usada para apresentação e comparação rápida.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS unidade_referencia (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    unidade_id  INTEGER,            -- unidade que serve de referência
    descricao   TEXT,               -- descrição do porquê foi escolhida como referência
    created_at  TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (unidade_id) REFERENCES unidades(id)
);

-- ------------------------------------------------------------
-- TABELA: unidade_referencia_tipo
-- Tipos de referência de unidade (ex: menor, maior, mais vendida)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS unidade_referencia_tipo (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome    TEXT NOT NULL            -- ex: compacta, padrão, premium
);

-- ------------------------------------------------------------
-- TABELA: historico_unidade
-- Rastreamento de alterações em unidades (auditoria)
-- Captura qualquer mudança de campo para análise futura da IA
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS historico_unidade (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    unidade_id  INTEGER NOT NULL,
    campo       TEXT NOT NULL,      -- nome do campo alterado
    valor_antigo TEXT,
    valor_novo  TEXT,
    changed_at  TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (unidade_id) REFERENCES unidades(id)
);

-- ------------------------------------------------------------
-- RELACIONAMENTO: corretores ↔ unidades
-- Corretor responsável pela venda de uma unidade específica
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS corretor_unidade (
    corretor_id INTEGER NOT NULL,
    unidade_id  INTEGER NOT NULL,
    tipo_vinculo TEXT,              -- ex: responsável, parceiro
    observacoes TEXT,
    PRIMARY KEY (corretor_id, unidade_id),
    FOREIGN KEY (corretor_id)   REFERENCES corretores(id),
    FOREIGN KEY (unidade_id)    REFERENCES unidades(id)
);

-- ============================================================
-- BLOCO 4: MAILING E LEADS
-- Pipeline de captação e qualificação de contatos
-- ============================================================

-- ------------------------------------------------------------
-- TABELA: mailing
-- Base bruta de contatos captados (tráfego pago, eventos, etc.)
-- É a entrada do pipeline: Mailing → Lead → Offer → Matching → IA
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mailing (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Identificação básica
    nome                TEXT,
    email               TEXT,
    telefone            TEXT,
    origem              TEXT,       -- ex: facebook, google, indicação
    tags                TEXT,       -- tags livres separadas por vírgula

    -- Controle de ingestão
    data_ingestao       TEXT,
    fonte_arquivo       TEXT,       -- nome do arquivo importado
    valido              INTEGER DEFAULT 1,  -- 1=válido, 0=inválido
    motivo_invalidacao  TEXT,
    hash_unico          TEXT,       -- evita duplicatas na ingestão

    -- Perfil pessoal
    sexo                TEXT,
    data_nascimento     TEXT,
    idade               INTEGER,
    estado_civil        TEXT,
    nacionalidade       TEXT,
    profissao           TEXT,
    empresa             TEXT,
    cargo               TEXT,
    renda_mensal        REAL,
    faixa_renda         TEXT,
    escolaridade        TEXT,

    -- Endereço atual
    cep                 TEXT,
    logradouro          TEXT,
    numero              TEXT,
    complemento         TEXT,
    bairro              TEXT,
    cidade              TEXT,
    estado              TEXT,
    pais                TEXT,

    -- Intenção imobiliária
    intencao            TEXT,       -- comprar / alugar / investir
    tipo_imovel         TEXT,
    faixa_preco         TEXT,
    preco_min           REAL,
    preco_max           REAL,
    quartos             INTEGER,
    vagas               INTEGER,
    metragem_min        REAL,
    metragem_max        REAL,
    bairro_interesse    TEXT,
    cidade_interesse    TEXT,
    urgencia            TEXT,       -- baixa / média / alta / imediata
    motivo              TEXT,       -- ex: casamento, filho, investimento

    -- Rastreamento de marketing
    utm_source          TEXT,
    utm_medium          TEXT,
    utm_campaign        TEXT,
    utm_term            TEXT,
    utm_content         TEXT,
    primeiro_contato    TEXT,
    ultimo_contato      TEXT,
    canal_preferido     TEXT,
    score_mailing       REAL,

    -- Auditoria
    criado_em           TEXT DEFAULT (datetime('now')),
    atualizado_em       TEXT DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------
-- TABELA: lead
-- Contato qualificado — originado do mailing ou diretamente.
-- Entra no pipeline de oferta, matching e IA.
-- ATENÇÃO: campos de localização usam sufixo _interesse
-- O IAEngine normaliza: cidade_interesse → cidade antes de vetorizar
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS lead (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Identificação
    nome                TEXT,
    email               TEXT,
    telefone            TEXT,
    origem              TEXT,
    data_ingestao       TEXT,
    status              TEXT,       -- novo / em_contato / qualificado / perdido / convertido
    tags                TEXT,

    -- Intenção imobiliária
    intencao            TEXT,
    tipo_imovel         TEXT,
    faixa_preco         TEXT,
    preco_min           REAL,
    preco_max           REAL,
    quartos             INTEGER,
    vagas               INTEGER,
    metragem_min        REAL,
    metragem_max        REAL,

    -- Localização de interesse (normalizar antes de usar no IAEngine)
    bairro_interesse    TEXT,
    regiao_interesse    VARCHAR(255),
    cidade_interesse    TEXT,

    -- Qualificação
    urgencia            TEXT,
    motivo              TEXT,

    -- Rastreamento de marketing
    utm_source          TEXT,
    utm_medium          TEXT,
    utm_campaign        TEXT,
    utm_term            TEXT,
    utm_content         TEXT,
    canal_preferido     TEXT,

    -- Dados ricos herdados do mailing
    profile_json        TEXT,       -- JSON com dados completos do mailing de origem
    historico_json      TEXT,       -- JSON com histórico de interações
    score_lead          REAL,       -- score de qualificação calculado

    -- Auditoria
    criado_em           TEXT DEFAULT (datetime('now')),
    atualizado_em       TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- BLOCO 5: ENGINES — OFFER, MATCHING, IA
-- Saídas dos motores de inteligência comercial
-- ============================================================

-- ------------------------------------------------------------
-- TABELA: offer
-- Ofertas geradas pelo Offer Engine para cada lead.
-- Ainda referencia empreendimentos — avaliar migração para
-- unidades em sprint futura quando Offer Engine for atualizado.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS offer (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id             INTEGER NOT NULL,
    empreendimento_id   INTEGER NOT NULL,   -- TODO: migrar para unidade_id (sprint futura)
    score               REAL NOT NULL,
    rationale           TEXT NOT NULL,      -- JSON com explicação da oferta
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (lead_id)           REFERENCES lead(id),
    FOREIGN KEY (empreendimento_id) REFERENCES empreendimentos(id)
);

-- ------------------------------------------------------------
-- TABELA: matching
-- Resultados do Matching Engine — cruzamento lead × unidade.
-- Opera por unidade (Sprint 10.5).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matching (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    unidade_id  INTEGER,            -- unidade avaliada
    lead_id     INTEGER,            -- lead avaliado
    score       REAL,               -- score de compatibilidade (0-100)
    created_at  TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (unidade_id)    REFERENCES unidades(id),
    FOREIGN KEY (lead_id)       REFERENCES lead(id)
);

-- ------------------------------------------------------------
-- TABELA: ia_score
-- Scores gerados pelo IA Engine — vetorização e conversão.
-- Opera por unidade (Sprint 10.5).
-- ATENÇÃO: campo é unidade_id, não property_id (corrigido Sprint 10.5)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ia_score (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    unidade_id      INTEGER,            -- unidade vetorizada
    lead_id         INTEGER,            -- lead vetorizado
    similarity      REAL,               -- cosine similarity entre vetores (0-1)
    conversion_score REAL,              -- previsão de conversão (0-100)
    lead_vector     TEXT,               -- JSON do vetor numérico do lead
    property_vector TEXT,               -- JSON do vetor numérico da unidade
    reasons_json    TEXT,               -- JSON explicável em linguagem comercial
    created_at      TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (unidade_id)    REFERENCES unidades(id),
    FOREIGN KEY (lead_id)       REFERENCES lead(id)
);

-- ============================================================
-- BLOCO 6: CONTROLE OPERACIONAL
-- ============================================================

-- ------------------------------------------------------------
-- TABELA: importacoes
-- Log de todas as importações realizadas via ingestão
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS importacoes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo            TEXT,           -- ex: mailing, lead, empreendimento, unidade
    arquivo         TEXT,           -- nome do arquivo importado
    origem          TEXT,           -- caminho ou fonte
    total_registros INTEGER,
    status          TEXT,           -- sucesso / erro / parcial
    data_execucao   TEXT,
    sucesso         INTEGER,        -- registros importados com sucesso
    erros           INTEGER,        -- registros com erro
    log             TEXT            -- log detalhado da importação
);

-- ============================================================
-- ÍNDICES DE PERFORMANCE
-- Apenas índices essenciais — expandir conforme necessidade
-- ============================================================

-- Índices para buscas frequentes em lead
CREATE INDEX IF NOT EXISTS idx_lead_status          ON lead(status);
CREATE INDEX IF NOT EXISTS idx_lead_cidade          ON lead(cidade_interesse);
CREATE INDEX IF NOT EXISTS idx_lead_preco           ON lead(preco_min, preco_max);

-- Índices para buscas em unidades
CREATE INDEX IF NOT EXISTS idx_unidade_empreendimento   ON unidades(empreendimento_id);
CREATE INDEX IF NOT EXISTS idx_unidade_disponibilidade  ON unidades(disponibilidade);
CREATE INDEX IF NOT EXISTS idx_unidade_preco            ON unidades(preco);

-- Índices para IA e Matching
CREATE INDEX IF NOT EXISTS idx_ia_score_lead        ON ia_score(lead_id);
CREATE INDEX IF NOT EXISTS idx_ia_score_unidade     ON ia_score(unidade_id);
CREATE INDEX IF NOT EXISTS idx_matching_lead        ON matching(lead_id);
CREATE INDEX IF NOT EXISTS idx_matching_unidade     ON matching(unidade_id);

-- Índice de deduplicação de mailing
CREATE INDEX IF NOT EXISTS idx_mailing_hash         ON mailing(hash_unico);

-- ============================================================
-- FIM DO SCHEMA
-- ============================================================