
---

## `docs/database/schema-atual.md`

```markdown
# Schema Atual — Banco de Dados (SQLite)

> Estado do banco até a Sprint 10 (antes da Sprint 10.5)

---

## Tabela `lead`

```sql
CREATE TABLE lead (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    telefone TEXT,
    origem TEXT,
    tags TEXT,
    intencao TEXT,
    tipo_imovel TEXT,
    faixa_preco TEXT,
    preco_min REAL,
    preco_max REAL,
    quartos INTEGER,
    vagas INTEGER,
    metragem_min REAL,
    metragem_max REAL,
    bairro_interesse TEXT,
    cidade_interesse TEXT,
    urgencia TEXT,
    motivo TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    utm_term TEXT,
    utm_content TEXT,
    canal_preferido TEXT
);

Tabela empreendimentos (estado atual — com limitações)
Campos conhecidos:

id, nome, regiao, bairro, cidade, estado
tipo, produto, endereco
data_entrega, status_entrega
descricao
incorporadora_id, spe_id
periodo_lancamento
unidade_referencia_id
preco ⚠️ (será descontinuado)
tipologia ⚠️ (será descontinuado)
metragem_min ⚠️ (será descontinuado)
metragem_max ⚠️ (será descontinuado)
Tabela ia_score (Sprint 10)

CREATE TABLE ia_score (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    property_id INTEGER,
    similarity REAL,
    conversion_score REAL,
    lead_vector TEXT,
    property_vector TEXT,
    reasons_json TEXT,
    created_at TEXT
);
📌 Rodapé: Pendências estruturais identificadas na Sprint 10.
Schema alvo definido em Schema Alvo 10.5.
Decisão arquitetural em ADR-002.