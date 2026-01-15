PRAGMA foreign_keys = ON;

-- ============================================================
-- TABELA: construtoras
-- ============================================================
CREATE TABLE IF NOT EXISTS construtoras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT,
    contato TEXT,
    observacoes TEXT
);

-- ============================================================
-- TABELA: imobiliarias
-- ============================================================
CREATE TABLE IF NOT EXISTS imobiliarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT,
    contato TEXT,
    observacoes TEXT
);

-- ============================================================
-- RELACIONAMENTO N:N — construtoras ↔ imobiliarias
-- ============================================================
CREATE TABLE IF NOT EXISTS construtora_imobiliaria (
    construtora_id INTEGER NOT NULL,
    imobiliaria_id INTEGER NOT NULL,
    tipo_parceria TEXT,
    observacoes TEXT,
    PRIMARY KEY (construtora_id, imobiliaria_id),
    FOREIGN KEY (construtora_id) REFERENCES construtoras(id),
    FOREIGN KEY (imobiliaria_id) REFERENCES imobiliarias(id)
);

-- ============================================================
-- TABELA: corretores
-- ============================================================
CREATE TABLE IF NOT EXISTS corretores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    creci TEXT,
    observacoes TEXT
);

-- ============================================================
-- RELACIONAMENTO N:N — corretores ↔ imobiliarias
-- ============================================================
CREATE TABLE IF NOT EXISTS corretor_imobiliaria (
    corretor_id INTEGER NOT NULL,
    imobiliaria_id INTEGER NOT NULL,
    tipo_vinculo TEXT,
    observacoes TEXT,
    PRIMARY KEY (corretor_id, imobiliaria_id),
    FOREIGN KEY (corretor_id) REFERENCES corretores(id),
    FOREIGN KEY (imobiliaria_id) REFERENCES imobiliarias(id)
);

-- ============================================================
-- TABELA: imoveis
-- ============================================================
CREATE TABLE IF NOT EXISTS imoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    regiao TEXT,
    bairro TEXT,
    cidade TEXT,
    estado TEXT,
    produto TEXT NOT NULL,
    endereco TEXT,
    data_entrega TEXT,
    status_entrega TEXT,
    tipo TEXT,
    descricao TEXT
);

-- ============================================================
-- TABELA: unidades_referencia
-- ============================================================
CREATE TABLE IF NOT EXISTS unidades_referencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imovel_id INTEGER NOT NULL,
    construtora_id INTEGER NOT NULL,
    codigo_unidade TEXT,
    metragem REAL,
    valor REAL,
    observacoes TEXT,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id),
    FOREIGN KEY (construtora_id) REFERENCES construtoras(id)
);