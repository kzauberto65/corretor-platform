
---

## `docs/database/schema-alvo-10-5.md`

```markdown
# Schema Alvo — Sprint 10.5

> Novo modelo de dados com separação empreendimentos × unidades

---

## Nova Tabela `unidades`

```sql
CREATE TABLE unidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendimento_id INTEGER NOT NULL,
    codigo_unidade TEXT,
    preco REAL,
    metragem REAL,
    dormitorios INTEGER,
    suites INTEGER,
    vagas INTEGER,
    tipo_unidade TEXT,       -- studio, 1 dorm, garden, cobertura, casa
    andar INTEGER,
    disponibilidade TEXT,    -- disponível / vendido / reservado
    descricao_unidade TEXT,
    created_at TEXT,
    FOREIGN KEY (empreendimento_id) REFERENCES empreendimentos(id)
);

Nova Tabela unidade_referencia (Histórico)

CREATE TABLE unidade_referencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendimento_id INTEGER NOT NULL,
    unidade_id INTEGER NOT NULL,
    codigo TEXT,
    preco REAL,
    metragem REAL,
    dormitorios INTEGER,
    vagas INTEGER,
    tipo_unidade TEXT,
    data_referencia TEXT,
    created_at TEXT,
    FOREIGN KEY (empreendimento_id) REFERENCES empreendimentos(id),
    FOREIGN KEY (unidade_id) REFERENCES unidades(id)
);
Tabela empreendimentos (ajustada)
Campos removidos/descontinuados
preco
tipologia
metragem_min
metragem_max
Campos mantidos
id, nome, regiao, bairro, cidade, estado
produto, endereco, tipo
data_entrega, status_entrega
descricao
incorporadora_id, spe_id
periodo_lancamento
unidade_referencia_id → agora aponta para unidades.id
Campos novos
total_unidades (INTEGER)
amenities (TEXT/JSON)
padrao_construtivo (TEXT/JSON)
Relacionamentos

empreendimentos 1 ──→ N unidades
unidades        1 ──→ N unidade_referencia
empreendimentos 1 ──→ N unidade_referencia
📌 Rodapé: Migração detalhada em
Sprint 10.5 — Migração.
Decisão arquitetural em ADR-002.