
---

## `docs/sprints/sprint10.5/sprint-10-5-schema.md`

```markdown
# Sprint 10.5 — Schema (Modelo de Dados)

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
    tipo_unidade TEXT,
    andar INTEGER,
    disponibilidade TEXT,
    descricao_unidade TEXT,
    created_at TEXT,
    FOREIGN KEY (empreendimento_id) REFERENCES empreendimentos(id)
);

Valores de tipo_unidade
studio
1 dorm
garden
cobertura
casa
Valores de disponibilidade
disponível
vendido
reservado
Nova Tabela unidade_referencia

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
Ajustes em empreendimentos
Remover/descontinuar
Campo	Motivo
preco	Migra para unidades.preco
tipologia	Migra para unidades.tipo_unidade
metragem_min	Migra para unidades.metragem
metragem_max	Migra para unidades.metragem
Adicionar
Campo	Tipo	Descrição
total_unidades	INTEGER	Total de unidades do empreendimento
amenities	TEXT/JSON	Lista de amenidades
padrao_construtivo	TEXT/JSON	Padrão construtivo
📌 Rodapé: Schema completo consolidado em
Schema Alvo 10.5.
Migração em Sprint 10.5 — Migração.