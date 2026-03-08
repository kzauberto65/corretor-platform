# ADR-001 — Contrato de Arquitetura

**Status:** Aceito
**Data:** Fevereiro/2026
**Versão:** 1.1

---

## Contexto

A plataforma segue Clean Architecture com 4 camadas:

| Camada | Responsabilidade |
|--------|-----------------|
| **Domain** | Entities, DTOs, Value Objects, Interfaces de repositório |
| **Application** | Services, Normalizers, Use Cases |
| **Infrastructure** | Repositórios concretos, Ingestores, Exporters, Banco de dados |
| **Interface** | CLI, API, Webhooks |

---

## Estrutura Oficial de Pastas

```text
src/
├── application/
│   └── <modulo>/
│       ├── services/
│       └── normalizers/
├── domain/
│   └── <modulo>/
│       ├── dto/
│       └── entities/
├── infrastructure/
│   └── <modulo>/
│   │   └── repositories/
│   └── ingestao/
│       ├── base_ingestor.py
│       ├── normalizador.py
│       ├── xls_parser.py
│       ├── ingestao_lead.py
│       └── ingestao_mailings.py
└── interface/
    └── cli/
        └── menu.py

Perfeito. Vou gerar tudo agora com base na sua estrutura existente e nos 5 documentos que você enviou.

---

# Estrutura final de `docs/`

```
docs/
├── index.md
├── adr/
│   ├── adr-001-contrato-arquitetura.md
│   ├── adr-002-refatoracao-imoveis.md
│   └── adr-003-ia-engine-v1.md
├── c4/
│   ├── c4-nivel2-containers.md
│   ├── c4-nivel3-componentes.md
│   └── c4-nivel4-pipeline.md
├── sprints/
│   ├── sprint7/
│   │   └── sprint-7-lead-engine.md
│   ├── sprint8/
│   │   └── sprint-8-offer-engine.md
│   ├── sprint9/
│   │   └── sprint-9-matching-engine.md
│   ├── sprint10/
│   │   ├── sprint-10-ia-engine.md
│   │   └── sprint-10-problemas-correcoes.md
│   └── sprint10.5/
│       ├── sprint-10-5-planejamento.md
│       ├── sprint-10-5-schema.md
│       ├── sprint-10-5-repositorios.md
│       ├── sprint-10-5-migracao.md
│       ├── sprint-10-5-ia-matching.md
│       └── sprint-10-5-cli-testes.md
├── database/
│   ├── schema-atual.md
│   └── schema-alvo-10-5.md
└── master/
    ├── documento-mestre.md
    └── roadmap.md
```

---

# Arquivos gerados

## `docs/index.md`

```markdown
# 📘 Índice Geral — Documentação Corretor Platform

> Fonte única de verdade do projeto.
> Última atualização: Sprint 10.5 (planejamento)

---

## 🏗️ Arquitetura (ADRs)

| Documento | Descrição |
|-----------|-----------|
| [ADR-001 — Contrato de Arquitetura](adr/adr-001-contrato-arquitetura.md) | Clean Architecture, padrões de DTO, Normalizer, Service, Repository, Pipeline de Ingestão |
| [ADR-002 — Refatoração de Imóveis](adr/adr-002-refatoracao-imoveis.md) | Decisão de separar empreendimentos × unidades (Sprint 10.5) |
| [ADR-003 — IA Engine v1](adr/adr-003-ia-engine-v1.md) | Arquitetura do motor de IA, vetorização, limitações e evolução |
| [ADR-004 — Ingestão Idempotente](adr/adr-004-ingestao-idempotente.md) | Cache de sessão na ingestão para evitar duplicação em lote |
---

## 📐 C4 — Diagramas de Arquitetura

| Documento | Descrição |
|-----------|-----------|
| [C4 Nível 2 — Containers](c4/c4-nivel2-containers.md) | CLI, API, Engines, Banco, Automação |
| [C4 Nível 3 — Componentes](c4/c4-nivel3-componentes.md) | IAEngine, IAService, IARepository, Matching, Unidades |
| [C4 Nível 4 — Pipeline](c4/c4-nivel4-pipeline.md) | Mailing → Lead → Offer → Matching → IA → Automação |

---

## 🗄️ Banco de Dados

| Documento | Descrição |
|-----------|-----------|
| [Schema Atual](database/schema-atual.md) | Tabelas atuais: lead, empreendimentos, ia_score, matching |
| [Schema Alvo 10.5](database/schema-alvo-10-5.md) | Novo schema: unidades, unidade_referencia, empreendimentos ajustado |

---

## 🏃 Sprints

### Ativas

| Sprint | Documento | Status |
|--------|-----------|--------|
| **10.5** | [Planejamento](sprints/sprint10.5/sprint-10-5-planejamento.md) | 🔵 Em andamento |
| **10.5** | [Schema](sprints/sprint10.5/sprint-10-5-schema.md) | 🔵 Em andamento |
| **10.5** | [Repositórios](sprints/sprint10.5/sprint-10-5-repositorios.md) | 🔵 Em andamento |
| **10.5** | [Migração](sprints/sprint10.5/sprint-10-5-migracao.md) | 🔵 Em andamento |
| **10.5** | [IA + Matching](sprints/sprint10.5/sprint-10-5-ia-matching.md) | 🔵 Em andamento |
| **10.5** | [CLI + Testes](sprints/sprint10.5/sprint-10-5-cli-testes.md) | 🔵 Em andamento |

### Concluídas

| Sprint | Documento | Status |
|--------|-----------|--------|
| **10** | [IA Engine v1](sprints/sprint10/sprint-10-ia-engine.md) | ✅ Concluída |
| **10** | [Problemas e Correções](sprints/sprint10/sprint-10-problemas-correcoes.md) | ✅ Concluída |

### Anteriores (referência)

| Sprint | Documento | Status |
|--------|-----------|--------|
| **7** | [Lead Engine](sprints/sprint7/sprint-7-lead-engine.md) | 📦 Arquivada |
| **8** | [Offer Engine](sprints/sprint8/sprint-8-offer-engine.md) | 📦 Arquivada |
| **9** | [Matching Engine](sprints/sprint9/sprint-9-matching-engine.md) | 📦 Arquivada |

---

## 📖 Documento Mestre

| Documento | Descrição |
|-----------|-----------|
| [Documento Mestre](master/documento-mestre.md) | Visão completa da plataforma, seções 1–27 |
| [Roadmap](master/roadmap.md) | 32 sprints planejadas |

---

> **Nota:** Para usar com Continue/Claude, referencie os arquivos com `@docs/...`
> Exemplo: `@docs/database/schema-alvo-10-5.md`
```

---

## `docs/adr/adr-001-contrato-arquitetura.md`

```markdown
# ADR-001 — Contrato de Arquitetura

**Status:** Aceito
**Data:** Fevereiro/2026
**Versão:** 1.1

---

## Contexto

A plataforma segue Clean Architecture com 4 camadas:

| Camada | Responsabilidade |
|--------|-----------------|
| **Domain** | Entities, DTOs, Value Objects, Interfaces de repositório |
| **Application** | Services, Normalizers, Use Cases |
| **Infrastructure** | Repositórios concretos, Ingestores, Exporters, Banco de dados |
| **Interface** | CLI, API, Webhooks |

---

## Estrutura Oficial de Pastas

```text
src/
├── application/
│   └── <modulo>/
│       ├── services/
│       └── normalizers/
├── domain/
│   └── <modulo>/
│       ├── dto/
│       └── entities/
├── infrastructure/
│   └── <modulo>/
│   │   └── repositories/
│   └── ingestao/
│       ├── base_ingestor.py
│       ├── normalizador.py
│       ├── xls_parser.py
│       ├── ingestao_lead.py
│       └── ingestao_mailings.py
└── interface/
    └── cli/
        └── menu.py
```

---

## Padrões Obrigatórios

### Entity (Modelos de Domínio)
- Usar `@dataclass`.
- **Regra de Ouro:** Campos opcionais ou gerados pelo banco (como `id`) devem usar sintaxe explícita com valor padrão `None` para não quebrarem o `__init__`.
- Padrão moderno (PEP 604): `id: int | None = None`
- Outros campos opcionais: `nome: str | None = None`
- Local: `domain/<modulo>/entities/`

### DTO (Data Transfer Object)
- Nomes em inglês, snake_case
- Apenas dados, sem lógica
- Validação mínima
- Local: `domain/<modulo>/dto/`

### Normalizer
- Recebe dict bruto → retorna DTO limpo
- Não acessa banco nem filesystem
- Local: `application/<modulo>/normalizers/`

### Service
- Recebe DTO → aplica regras de negócio → chama repositório
- Não conhece ingestão nem CLI
- Local: `application/<modulo>/services/`

### Repository
- Implementa interface do domain
- Apenas CRUD, sem regra de negócio
- Local: `infrastructure/<modulo>/repositories/`

---

## Pipeline de Ingestão

```text
XLSX → Ingestor → Normalizer → DTO → Service → Repository → DB
```

---

## Regras de Ingestão
- Colunas opcionais podem vir vazias
- Colunas obrigatórias devem existir
- Arquivos com erro → `/erros`
- Arquivos processados → `/processados`
- **Idempotência de Sessão:** Ingestores devem obrigatoriamente usar In-Memory Cache (Dicionários) durante o loop de leitura para não recadastrar e não duplicar entidades mestre na mesma execução (ver [ADR-004](adr-004-ingestao-idempotente.md)).
---

## Regra para Geração de Código (IA)

Ao pedir "Gerar módulo X seguindo nosso contrato de arquitetura", a IA deve:
- Seguir estrutura de pastas oficial
- Seguir padrões de DTO, Normalizer, Service, Repository
- Seguir pipeline de ingestão
- Nomes em português para domínio, inglês para código
- snake_case
- **Sem inventar colunas**
- **Sem alterar arquitetura**

---

## Glossário

| Termo | Definição |
|-------|-----------|
| DTO | Data Transfer Object |
| Normalizer | Transforma dados brutos em DTO |
| Service | Regra de negócio |
| Repository | Acesso ao banco |
| Ingestor | Lê arquivos e dispara pipeline |
| CLI | Interface de linha de comando |

---

> 📌 **Rodapé:** Este ADR é a base de toda geração de código da plataforma.
> Referenciado por: [Sprint 10](../sprints/sprint10/sprint-10-ia-engine.md),
> [Sprint 10.5](../sprints/sprint10.5/sprint-10-5-planejamento.md),
> [Schema Alvo](../database/schema-alvo-10-5.md)
```

---

## `docs/adr/adr-002-refatoracao-imoveis.md`

```markdown
# ADR-002 — Refatoração de Imóveis (Empreendimentos × Unidades)

**Status:** Proposto (Sprint 10.5)
**Data:** 2026
**Origem:** Problemas identificados na Sprint 10

---

## Contexto

A tabela `empreendimentos` não suporta múltiplas unidades:
- Preço único por empreendimento
- Metragem única
- Tipologia única
- Ausência de dormitórios, vagas, disponibilidade, andar
- Impossível representar gardens, coberturas, studios

O IAEngine v1 e o Matching Engine operam sobre dados incompletos.

---

## Decisão

Separar o modelo em 3 entidades:

| Entidade | Papel |
|----------|-------|
| **empreendimentos** | Contexto institucional (nome, localização, incorporadora, entrega) |
| **unidades** | Item comercializável real (preço, metragem, dormitórios, vagas, tipo, disponibilidade) |
| **unidade_referencia** | Histórico/snapshot para aprendizado da IA |

### Consequências
- Empreendimento **deixa** de ser item comercial
- Unidade **passa a ser** o item comercial real
- IAEngine e Matching passam a operar **por unidade**
- Compatibilidade com banco atual preservada via migração
- Preparação para embeddings reais (Sprint 11)

---

> 📌 **Rodapé:** Detalhamento completo do schema em
> [Schema Alvo 10.5](../database/schema-alvo-10-5.md).
> Planejamento da sprint em
> [Sprint 10.5 — Planejamento](../sprints/sprint10.5/sprint-10-5-planejamento.md).
```

---

## `docs/adr/adr-003-ia-engine-v1.md`

```markdown
# ADR-003 — IA Engine v1

**Status:** Aceito (Sprint 10 — Concluída)
**Data:** 2026

---

## Contexto

Necessidade de um motor de IA para:
- Vetorizar leads e imóveis numericamente
- Calcular similaridade vetorial (cosine similarity)
- Prever conversão inicial
- Gerar reasons_json explicável
- Persistir resultados em `ia_score`

---

## Decisão

Implementar IAEngine v1 com:
- Vetorização numérica (sem embeddings textuais)
- Cosine similarity
- Heurísticas complementares (localização, urgência, entrega)
- Normalização automática de campos `*_interesse`
- Persistência em tabela `ia_score`

### Arquitetura

```text
src/
├── application/ia/
│   ├── services/ia_service.py
│   └── engine/ia_engine.py
├── domain/ia/
│   ├── dto/
│   └── entities/
├── infrastructure/ia/
│   └── repositories/ia_repository.py
└── interface/cli/
    └── ia_cli.py
```

### Pipeline

```text
Lead + Imóveis → IAEngine → IAInputDTO → IARepository → SQLite
```

---

## Limitações conhecidas (v1)
- Não utiliza embeddings textuais
- Não interpreta descrição do imóvel
- Não interpreta profile_json
- Similaridade baixa para vetores de magnitude muito diferente
- Dependência da estrutura atual de `empreendimentos`

## Evolução prevista (Sprint 11)
- Embeddings reais
- Vetorização semântica
- Pesos dinâmicos
- Aprendizado contínuo

---

> 📌 **Rodapé:** Problemas e correções detalhados em
> [Sprint 10 — Problemas e Correções](../sprints/sprint10/sprint-10-problemas-correcoes.md).
> Evolução planejada em
> [Sprint 10.5 — IA + Matching](../sprints/sprint10.5/sprint-10-5-ia-matching.md).
```

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
```

---

## Tabela `empreendimentos` (estado atual — com limitações)

Campos conhecidos:
- id, nome, regiao, bairro, cidade, estado
- tipo, produto, endereco
- data_entrega, status_entrega
- descricao
- incorporadora_id, spe_id
- periodo_lancamento
- unidade_referencia_id
- preco ⚠️ (será descontinuado)
- tipologia ⚠️ (será descontinuado)
- metragem_min ⚠️ (será descontinuado)
- metragem_max ⚠️ (será descontinuado)

---

## Tabela `ia_score` (Sprint 10)

```sql
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
```

---

> 📌 **Rodapé:** Pendências estruturais identificadas na Sprint 10.
> Schema alvo definido em [Schema Alvo 10.5](schema-alvo-10-5.md).
> Decisão arquitetural em [ADR-002](../adr/adr-002-refatoracao-imoveis.md).
```

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
```

---

## Nova Tabela `unidade_referencia` (Histórico)

```sql
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
```

---

## Tabela `empreendimentos` (ajustada)

### Campos removidos/descontinuados
- ~~preco~~
- ~~tipologia~~
- ~~metragem_min~~
- ~~metragem_max~~

### Campos mantidos
- id, nome, regiao, bairro, cidade, estado
- produto, endereco, tipo
- data_entrega, status_entrega
- descricao
- incorporadora_id, spe_id
- periodo_lancamento
- unidade_referencia_id → agora aponta para `unidades.id`

### Campos novos
- `total_unidades` (INTEGER)
- `amenities` (TEXT/JSON)
- `padrao_construtivo` (TEXT/JSON)

---

## Relacionamentos

```text
empreendimentos 1 ──→ N unidades
unidades        1 ──→ N unidade_referencia
empreendimentos 1 ──→ N unidade_referencia
```

---

> 📌 **Rodapé:** Migração detalhada em
> [Sprint 10.5 — Migração](../sprints/sprint10.5/sprint-10-5-migracao.md).
> Decisão arquitetural em [ADR-002](../adr/adr-002-refatoracao-imoveis.md).
```

---

## `docs/sprints/sprint7/sprint-7-lead-engine.md`

```markdown
# Sprint 7 — Lead Engine (Motor de Leads)

**Status:** 📦 Arquivada / Concluída

---

## Resumo

Implementação do módulo de leads da plataforma, incluindo:
- Tabela `lead` no SQLite
- LeadRepository (CRUD)
- LeadService
- LeadNormalizer
- LeadIngestor (pipeline XLSX → DB)
- CLI para ingestão de leads

---

## Entregas
- ☑ Tabela `lead` criada
- ☑ Pipeline de ingestão funcional
- ☑ CLI operacional
- ☑ Normalização de dados

---

> 📌 **Rodapé:** Contrato de arquitetura seguido: [ADR-001](../../adr/adr-001-contrato-arquitetura.md).
> Schema da tabela lead: [Schema Atual](../../database/schema-atual.md).
```

---

## `docs/sprints/sprint8/sprint-8-offer-engine.md`

```markdown
# Sprint 8 — Offer Engine (Motor de Ofertas)

**Status:** 📦 Arquivada / Concluída

---

## Resumo

Implementação do módulo de ofertas/empreendimentos, incluindo:
- Tabela `empreendimentos` no SQLite
- EmpreendimentoRepository (CRUD)
- Pipeline de ingestão de empreendimentos
- CLI para gestão de empreendimentos

---

## Entregas
- ☑ Tabela `empreendimentos` criada
- ☑ Pipeline de ingestão funcional
- ☑ CLI operacional

---

## Limitações identificadas (referência para Sprint 10.5)
- Tabela não suporta múltiplas unidades
- Preço/metragem/tipologia únicos por empreendimento

---

> 📌 **Rodapé:** Limitações tratadas em [ADR-002](../../adr/adr-002-refatoracao-imoveis.md)
> e [Sprint 10.5](../sprint10.5/sprint-10-5-planejamento.md).
```

---

## `docs/sprints/sprint9/sprint-9-matching-engine.md`

```markdown
# Sprint 9 — Matching Engine

**Status:** 📦 Arquivada / Concluída

---

## Resumo

Implementação do motor de matching lead × empreendimento:
- MatchingEngine
- MatchingService
- MatchingRepository
- reasons_json explicável
- CLI para execução de matching

---

## Entregas
- ☑ Matching lead × empreendimento funcional
- ☑ reasons_json gerado
- ☑ Persistência em SQLite
- ☑ CLI operacional

---

## Evolução planejada (Sprint 10.5)
- Matching passa a operar **por unidade**, não por empreendimento

---

> 📌 **Rodapé:** Evolução detalhada em
> [Sprint 10.5 — IA + Matching](../sprint10.5/sprint-10-5-ia-matching.md).
```

---

## `docs/sprints/sprint10/sprint-10-ia-engine.md`

```markdown
# Sprint 10 — IA Engine v1

**Status:** ✅ Concluída

---

## Objetivo

Implementar o IA Engine v1:
- Vetorização numérica de leads e imóveis
- Similaridade vetorial (cosine similarity)
- Previsão inicial de conversão (conversion_score)
- reasons_json explicável
- Persistência em `ia_score`
- Integração com pipeline Lead → Offer → Matching → IA

---

## Escopo Entregue

- ☑ IAEngine com vetorização numérica
- ☑ Cosine similarity funcional
- ☑ Conversion score com heurísticas
- ☑ Normalização automática de campos `*_interesse`
- ☑ reasons_json explicável
- ☑ Persistência completa em `ia_score`
- ☑ CLI operacional (`ia_cli.py`)
- ☑ Integração total com Matching Engine

---

## Arquitetura

```text
src/
├── application/ia/
│   ├── services/ia_service.py
│   └── engine/ia_engine.py
├── domain/ia/
│   ├── dto/
│   └── entities/
├── infrastructure/ia/
│   └── repositories/ia_repository.py
└── interface/cli/
    └── ia_cli.py
```

## Pipeline

```text
Lead + Imóveis → IAEngine → IAInputDTO → IARepository → SQLite
```

---

## Resultado Final

- ☑ IA Engine implementado
- ☑ Vetorização numérica funcional
- ☑ Similaridade vetorial
- ☑ Previsão de conversão
- ☑ Reasons explicáveis
- ☑ Persistência completa
- ☑ CLI operacional
- ☑ Correções críticas aplicadas
- ☑ Ranking validado com lead real
- ☑ Sprint concluída com sucesso

---

> 📌 **Rodapé:** Problemas encontrados e correções em
> [Sprint 10 — Problemas e Correções](sprint-10-problemas-correcoes.md).
> ADR do motor: [ADR-003](../../adr/adr-003-ia-engine-v1.md).
```

---

## `docs/sprints/sprint10/sprint-10-problemas-correcoes.md`

```markdown
# Sprint 10 — Problemas Encontrados e Correções

**Status:** ✅ Resolvidos

---

## 1. Campo inexistente usado pelo IAEngine

**Problema:** `quartos` não existe na tabela `empreendimentos`.
O Python atribuía 0 ou valores de outras colunas (ex: `incorporadora_id`).

**Impacto:** Vetor do imóvel distorcido. Imóvel 120 recebia boost fantasma.

**Correção:** Campo `quartos` removido do vetor. IAEngine reescrito para não depender de atributos inexistentes.

---

## 2. Localização do lead não utilizada

**Problema:** IAEngine esperava `cidade`, `bairro`, `regiao`.
Lead armazenava `cidade_interesse`, `bairro_interesse`, `regiao_interesse`.

**Impacto:** `location_score` era sempre 0. Imóvel 126 (Santos) perdia vantagem.

**Correção:** Método `_normalize_lead_input()` criado com mapeamento automático.

---

## 3. Similaridade baixa para imóveis perfeitos

**Problema:** Similarity de 0.08 para imóvel ideal (126).

**Causa:** Vetorização numérica pura + normalização por magnitude.
Valores altos de preço/metragem aumentavam módulo do vetor.

**Correção:** Ajuste de pesos. Localização passou a ter peso real.
Conversion_score do 126 subiu para 55.46%.

---

## 4. Entrega longa penalizando imóveis corretos

**Problema:** Urgência alta + entrega de ~14 meses penalizava demais.

**Correção:** Fórmula de entrega ajustada. Penalidade reduzida mas coerente.

---

## 5. Dados inconsistentes antes das correções

**Problema:** Vetores incompletos, localização vazia, atributos inexistentes.

**Correção:** Debug estruturado (EMP DEBUG / LEAD DEBUG), normalização de entrada, remoção de campos inválidos, reprocessamento completo.

---

## Aprendizados Técnicos

- Vetorização v1 **não pode depender de atributos inexistentes**
- Campos `*_interesse` devem ser **normalizados** antes do motor
- Similaridade vetorial pura não é suficiente — heurísticas complementares são essenciais
- Debug estruturado é **indispensável**
- Tabela `empreendimentos` precisa ser refatorada → **Sprint 10.5**
- Sprint 11 deve introduzir **embeddings reais**

---

> 📌 **Rodapé:** ADR relacionado: [ADR-003](../../adr/adr-003-ia-engine-v1.md).
> Refatoração planejada: [ADR-002](../../adr/adr-002-refatoracao-imoveis.md).
> Sprint de correção: [Sprint 10.5](../sprint10.5/sprint-10-5-planejamento.md).
```

---

## `docs/sprints/sprint10.5/sprint-10-5-planejamento.md`

```markdown
# Sprint 10.5 — Planejamento Geral

**Status:** 🔵 Em andamento
**Objetivo:** Refatoração estrutural do módulo de imóveis

---

## Objetivo Central

Corrigir a base estrutural do módulo de imóveis, preparando para:
- IA Vetorial v2 (Sprint 11)
- Embeddings reais
- Recomendação semântica
- Matching granular por unidade
- Precificação dinâmica futura
- Histórico de referência para aprendizado da IA
- Múltiplas unidades por empreendimento

---

## Entregas Obrigatórias

| # | Entrega | Doc detalhado |
|---|---------|---------------|
| 1 | Nova tabela `unidades` | [Schema](sprint-10-5-schema.md) |
| 2 | Tabela `unidade_referencia` (histórico) | [Schema](sprint-10-5-schema.md) |
| 3 | Ajustes em `empreendimentos` | [Schema](sprint-10-5-schema.md) |
| 4 | Repositórios novos/atualizados | [Repositórios](sprint-10-5-repositorios.md) |
| 5 | Matching Engine v1.5 (por unidade) | [IA + Matching](sprint-10-5-ia-matching.md) |
| 6 | IA Engine v1.5 (por unidade) | [IA + Matching](sprint-10-5-ia-matching.md) |
| 7 | Migração de dados | [Migração](sprint-10-5-migracao.md) |
| 8 | CLI atualizado + testes | [CLI + Testes](sprint-10-5-cli-testes.md) |

---

## Dependências

- ☑ IA Engine v1 (Sprint 10)
- ☑ Matching Engine (Sprint 9)
- ☑ Offer Engine (Sprint 8)
- ☑ Lead Engine (Sprint 7)
- ☑ Clean Architecture ([ADR-001](../../adr/adr-001-contrato-arquitetura.md))
- ☑ Modelo de dados atual ([Schema Atual](../../database/schema-atual.md))

---

## Componentes

```text
unidade_repository.py
empreendimento_repository.py (atualizado)
matching_engine.py (v1.5)
ia_engine.py (v1.5)
ia_service.py (v1.5)
unidade_cli.py
migração automática
```

## Pipeline Alvo

```text
Lead + Unidades → IAEngine (vetores + similaridade + conversão) → DTO → IARepository → SQLite
```

---

## Resultado Esperado

- ☐ Modelo de dados correto
- ☐ Unidades reais por empreendimento
- ☐ Vetorização consistente
- ☐ Matching granular
- ☐ IA preparada para embeddings
- ☐ Pipeline pronto para Sprint 11

---

> 📌 **Rodapé:** Decisão arquitetural: [ADR-002](../../adr/adr-002-refatoracao-imoveis.md).
> Schema alvo: [Schema Alvo 10.5](../../database/schema-alvo-10-5.md).
```

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
```

### Valores de `tipo_unidade`
- studio
- 1 dorm
- garden
- cobertura
- casa

### Valores de `disponibilidade`
- disponível
- vendido
- reservado

---

## Nova Tabela `unidade_referencia`

```sql
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
```

---

## Ajustes em `empreendimentos`

### Remover/descontinuar
| Campo | Motivo |
|-------|--------|
| `preco` | Migra para `unidades.preco` |
| `tipologia` | Migra para `unidades.tipo_unidade` |
| `metragem_min` | Migra para `unidades.metragem` |
| `metragem_max` | Migra para `unidades.metragem` |

### Adicionar
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `total_unidades` | INTEGER | Total de unidades do empreendimento |
| `amenities` | TEXT/JSON | Lista de amenidades |
| `padrao_construtivo` | TEXT/JSON | Padrão construtivo |

---

> 📌 **Rodapé:** Schema completo consolidado em
> [Schema Alvo 10.5](../../database/schema-alvo-10-5.md).
> Migração em [Sprint 10.5 — Migração](sprint-10-5-migracao.md).
```

---

## `docs/sprints/sprint10.5/sprint-10-5-repositorios.md`

```markdown
# Sprint 10.5 — Repositórios

---

## UnidadeRepository (novo)

Local: `src/infrastructure/unidade/repositories/unidade_repository.py`

### Métodos

```python
class UnidadeRepository:
    def save(self, dto) -> int: ...
    def update(self, id, dto) -> None: ...
    def delete(self, id) -> None: ...
    def list_all(self) -> list: ...
    def list_by_empreendimento(self, empreendimento_id) -> list: ...
    def list_disponiveis(self) -> list: ...
```

---

## EmpreendimentoRepository (atualizado)

Local: `src/infrastructure/empreendimento/repositories/empreendimento_repository.py`

### Novos métodos

```python
class EmpreendimentoRepository:
    # métodos existentes mantidos
    def list_unidades_by_empreendimento(self, id) -> list: ...
    def list_unidades_disponiveis(self) -> list: ...
    def get_unidade_referencia(self, empreendimento_id) -> dict: ...
```

---

## Regras (conforme ADR-001)
- Apenas CRUD
- Sem regra de negócio
- Implementa interface do domain

---

> 📌 **Rodapé:** Contrato de arquitetura: [ADR-001](../../adr/adr-001-contrato-arquitetura.md).
> Schema das tabelas: [Sprint 10.5 — Schema](sprint-10-5-schema.md).
```

---

## `docs/sprints/sprint10.5/sprint-10-5-migracao.md`

```markdown
# Sprint 10.5 — Migração de Dados

---

## Passos Obrigatórios

### 1. Criar tabela `unidades`
- Executar SQL de criação (ver [Schema](sprint-10-5-schema.md))

### 2. Migrar dados existentes
Para cada empreendimento existente, criar 1 unidade padrão:

```sql
INSERT INTO unidades (
    empreendimento_id,
    preco,
    metragem,
    tipo_unidade,
    disponibilidade,
    created_at
)
SELECT
    id,
    preco,
    metragem_min,
    tipologia,
    'disponível',
    datetime('now')
FROM empreendimentos;
```

### 3. Criar tabela `unidade_referencia`
- Executar SQL de criação (ver [Schema](sprint-10-5-schema.md))

### 4. Atualizar `unidade_referencia` para apontar para unidades reais

### 5. Atualizar IA e Matching para operar por unidade
- Ver [IA + Matching](sprint-10-5-ia-matching.md)

### 6. Manter compatibilidade com CLI atual

---

## Validações pós-migração
- Cada empreendimento deve ter pelo menos 1 unidade
- `unidade_referencia_id` deve ser válido
- Disponibilidade deve ser consistente
- Vetores devem ser regenerados

---

> 📌 **Rodapé:** Schema completo: [Schema Alvo 10.5](../../database/schema-alvo-10-5.md).
> Testes: [Sprint 10.5 — CLI + Testes](sprint-10-5-cli-testes.md).
```

---

## `docs/sprints/sprint10.5/sprint-10-5-ia-matching.md`

```markdown
# Sprint 10.5 — IA Engine v1.5 + Matching Engine v1.5

---

## Matching Engine v1.5

O Matching Engine passa a operar **por unidade**, não por empreendimento.

### Mudanças
- Matching agora é `lead × unidade`
- `reasons_json` passa a incluir:
  - Tipologia real
  - Metragem real
  - Preço real
  - Disponibilidade
  - Atributos da unidade
  - Atributos herdados do empreendimento (localização, entrega)

---

## IA Engine v1.5

O IAEngine passa a vetorizar **por unidade**.

### Vetor da unidade (v1.5)

| Dimensão | Origem |
|----------|--------|
| preço | `unidades.preco` |
| metragem | `unidades.metragem` |
| dormitórios | `unidades.dormitorios` |
| vagas | `unidades.vagas` |
| tipo_unidade | `unidades.tipo_unidade` |
| entrega | `empreendimentos.data_entrega` (herdado) |
| localização | `empreendimentos.cidade/bairro/regiao` (herdado) |

### Vetor do lead (v1.5)

| Dimensão | Origem |
|----------|--------|
| faixa de preço | `lead.preco_min / preco_max` |
| faixa de metragem | `lead.metragem_min / metragem_max` |
| tipo desejado | `lead.tipo_imovel` |
| urgência | `lead.urgencia` |
| localização | `lead.cidade_interesse / bairro_interesse` |
| preferências implícitas | `lead.profile_json` (futuro) |

---

> 📌 **Rodapé:** ADR do motor IA: [ADR-003](../../adr/adr-003-ia-engine-v1.md).
> Repositórios: [Sprint 10.5 — Repositórios](sprint-10-5-repositorios.md).
```

---

## `docs/sprints/sprint10.5/sprint-10-5-cli-testes.md`

```markdown
# Sprint 10.5 — CLI e Testes

---

## Novos Comandos CLI

```text
unidade add       → Adicionar unidade a um empreendimento
unidade list      → Listar unidades (com filtros)
unidade update    → Atualizar unidade
unidade delete    → Remover unidade
```

## Ajustes em Comandos Existentes

```text
matching run          → matching run-unidades
ia run                → ia run-unidades
```

---

## Testes Obrigatórios

### Testes mínimos
- [ ] Criação de unidades
- [ ] Migração de dados (empreendimento → unidade padrão)
- [ ] Matching por unidade
- [ ] IA por unidade
- [ ] reasons_json atualizado com dados da unidade
- [ ] CLI completo (add, list, update, delete)
- [ ] Integridade no SQLite

### Validações
- [ ] `unidade_referencia_id` válido
- [ ] Unidade pertence ao empreendimento correto
- [ ] Disponibilidade consistente (disponível/vendido/reservado)
- [ ] Vetores gerados corretamente após migração

---

> 📌 **Rodapé:** Schema das tabelas: [Sprint 10.5 — Schema](sprint-10-5-schema.md).
> Migração: [Sprint 10.5 — Migração](sprint-10-5-migracao.md).
> Contrato de arquitetura: [ADR-001](../../adr/adr-001-contrato-arquitetura.md).
```

---

## `docs/c4/c4-nivel2-containers.md`

```markdown
# C4 — Nível 2: Containers

```text
┌─────────────────────────────────────────┐
│            Corretor Platform            │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────┐  ┌─────┐  ┌────────────────┐  │
│  │ CLI │  │ API │  │   Automação    │  │
│  └──┬──┘  └──┬──┘  └───────┬────────┘  │
│     │        │              │           │
│  ┌──▼────────▼──────────────▼────────┐  │
│  │            Engines                │  │
│  │  ┌─────────┐  ┌───────────────┐   │  │
│  │  │ Mailing │  │  Lead Engine  │   │  │
│  │  └─────────┘  └───────────────┘   │  │
│  │  ┌─────────┐  ┌───────────────┐   │  │
│  │  │  Offer  │  │   Matching    │   │  │
│  │  └─────────┘  └───────────────┘   │  │
│  │  ┌──────────────────────────────┐ │  │
│  │  │     IA Engine (v1 / v1.5)   │ │  │
│  │  └──────────────────────────────┘ │  │
│  └───────────────┬───────────────────┘  │
│                  │                      │
│  ┌───────────────▼───────────────────┐  │
│  │         SQLite (Banco)            │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

> 📌 **Rodapé:** Componentes detalhados em [C4 Nível 3](c4-nivel3-componentes.md).
> Pipeline completo em [C4 Nível 4](c4-nivel4-pipeline.md).
```

---

## `docs/c4/c4-nivel3-componentes.md`

```markdown
# C4 — Nível 3: Componentes

## IA Engine

| Componente | Arquivo | Responsabilidade |
|------------|---------|-----------------|
| IAEngine | `ia_engine.py` | Vetorização + similaridade + conversão |
| IAService | `ia_service.py` | Orquestração da IA |
| IARepository | `ia_repository.py` | Persistência em `ia_score` |

## Matching Engine

| Componente | Arquivo | Responsabilidade |
|------------|---------|-----------------|
| MatchingEngine | `matching_engine.py` | Matching lead × unidade (v1.5) |

## Unidades (Sprint 10.5)

| Componente | Arquivo | Responsabilidade |
|------------|---------|-----------------|
| UnidadeRepository | `unidade_repository.py` | CRUD de unidades |
| EmpreendimentoRepository | `empreendimento_repository.py` | Atualizado com métodos de unidade |
| UnidadeCLI | `unidade_cli.py` | Interface CLI para unidades |

## Tabelas

| Tabela | Sprint |
|--------|--------|
| lead | 7 |
| empreendimentos | 8 (ajustado 10.5) |
| matching | 9 |
| ia_score | 10 |
| unidades | 10.5 |
| unidade_referencia | 10.5 |

---

> 📌 **Rodapé:** Container view em [C4 Nível 2](c4-nivel2-containers.md).
> Pipeline em [C4 Nível 4](c4-nivel4-pipeline.md).
```

---

## `docs/c4/c4-nivel4-pipeline.md`

```markdown
# C4 — Nível 4: Pipeline Completo

```text
Mailing
  │
  ▼
Lead Engine
  │
  ▼
Offer Engine (Empreendimentos + Unidades)
  │
  ▼
Matching Engine v1.5 (Lead × Unidade)
  │
  ▼
IA Engine v1.5 (Vetorização por Unidade)
  │
  ▼
ia_score (SQLite)
  │
  ▼
Automação (futuro)
```

## Pipeline detalhado (Sprint 10.5)

```text
Lead + Unidades
      │
      ▼
   IAEngine
   ├── vetorização do lead
   ├── vetorização da unidade (com dados herdados do empreendimento)
   ├── cosine similarity
   ├── conversion_score
   └── reasons_json
      │
      ▼
   IAInputDTO
      │
      ▼
   IARepository
      │
      ▼
   SQLite (ia_score)
```

---

> 📌 **Rodapé:** Componentes em [C4 Nível 3](c4-nivel3-componentes.md).
> IA + Matching detalhados em
> [Sprint 10.5 — IA + Matching](../sprints/sprint10.5/sprint-10-5-ia-matching.md).
```

---

## `docs/master/documento-mestre.md`

```markdown
# Documento Mestre — Plataforma de Inteligência Imobiliária

**Versão Definitiva — 2026**

> Este documento é o índice mestre. Conteúdo detalhado nos arquivos linkados.

---

## Seções e Referências

| Seção | Tema | Documento |
|-------|------|-----------|
| 7 | Roadmap (32 Sprints) | [Roadmap](roadmap.md) |
| 10 | Arquitetura da IA | [ADR-003](../adr/adr-003-ia-engine-v1.md) |
| 11 | Modelo de dados | [Schema Atual](../database/schema-atual.md), [Schema Alvo](../database/schema-alvo-10-5.md) |
| 12 | Arquitetura modular | [ADR-001](../adr/adr-001-contrato-arquitetura.md) |
| 14 | Pipelines críticos | [C4 Nível 4](../c4/c4-nivel4-pipeline.md) |
| 18 | Banco de dados | [Schema Atual](../database/schema-atual.md) |
| 19 | Governança de sprints | [Sprint 10 — Problemas](../sprints/sprint10/sprint-10-problemas-correcoes.md) |
| 27 | C4 completo | [Nível 2](../c4/c4-nivel2-containers.md), [Nível 3](../c4/c4-nivel3-componentes.md), [Nível 4](../c4/c4-nivel4-pipeline.md) |

---

## Atualizações Pendentes (Sprint 10.5)
- [ ] Seção 7 — incluir Sprint 10.5 no roadmap
- [ ] Seção 11 — empreendimentos + unidades
- [ ] Seção 14 — Matching → IA por unidade
- [ ] Seção 27 — C4 pipeline completo atualizado

---

> 📌 **Rodapé:** Índice geral do projeto em [docs/index.md](../index.md).
```

---

## `docs/master/roadmap.md`

```markdown
# Roadmap — 32 Sprints

---

## Sprints 7–12: Inteligência Comercial

| Sprint | Nome | Status |
|--------|------|--------|
| 7 | Lead Engine | ✅ Concluída |
| 8 | Offer Engine | ✅ Concluída |
| 9 | Matching Engine | ✅ Concluída |
| 10 | IA Engine v1 | ✅ Concluída |
| **10.5** | **Refatoração Empreendimentos/Unidades** | **🔵 Em andamento** |
| 11 | Dashboard CLI + IA Vetorial v2 | ⬜ Planejada |
| 12 | Exportações | ⬜ Planejada |

---

## Sprints 13+

> A definir conforme evolução do projeto.

---

## Visão de Evolução

```text
Sprint 10.5 (atual)
  → Modelo de dados correto
  → Unidades reais

Sprint 11
  → Embeddings reais
  → Vetorização semântica
  → Pesos dinâmicos

Sprint 12+
  → Aprendizado contínuo
  → Recomendação semântica
  → API pública
  → Automações
```

---

> 📌 **Rodapé:** Detalhes de cada sprint em [docs/sprints/](../sprints/).
> Índice geral em [docs/index.md](../index.md).
```

---

## Resumo do que foi gerado

| # | Arquivo | Caminho |
|---|---------|---------|
| 1 | Índice geral | `docs/index.md` |
| 2 | ADR-001 Contrato de Arquitetura | `docs/adr/adr-001-contrato-arquitetura.md` |
| 3 | ADR-002 Refatoração de Imóveis | `docs/adr/adr-002-refatoracao-imoveis.md` |
| 4 | ADR-003 IA Engine v1 | `docs/adr/adr-003-ia-engine-v1.md` |
| 5 | Schema Atual | `docs/database/schema-atual.md` |
| 6 | Schema Alvo 10.5 | `docs/database/schema-alvo-10-5.md` |
| 7 | Sprint 7 — Lead Engine | `docs/sprints/sprint7/sprint-7-lead-engine.md` |
| 8 | Sprint 8 — Offer Engine | `docs/sprints/sprint8/sprint-8-offer-engine.md` |
| 9 | Sprint 9 — Matching Engine | `docs/sprints/sprint9/sprint-9-matching-engine.md` |
| 10 | Sprint 10 — IA Engine | `docs/sprints/sprint10/sprint-10-ia-engine.md` |
| 11 | Sprint 10 — Problemas/Correções | `docs/sprints/sprint10/sprint-10-problemas-correcoes.md` |
| 12 | Sprint 10.5 — Planejamento | `docs/sprints/sprint10.5/sprint-10-5-planejamento.md` |
| 13 | Sprint 10.5 — Schema | `docs/sprints/sprint10.5/sprint-10-5-schema.md` |
| 14 | Sprint 10.5 — Repositórios | `docs/sprints/sprint10.5/sprint-10-5-repositorios.md` |
| 15 | Sprint 10.5 — Migração | `docs/sprints/sprint10.5/sprint-10-5-migracao.md` |
| 16 | Sprint 10.5 — IA + Matching | `docs/sprints/sprint10.5/sprint-10-5-ia-matching.md` |
| 17 | Sprint 10.5 — CLI + Testes | `docs/sprints/sprint10.5/sprint-10-5-cli-testes.md` |
| 18 | C4 Nível 2 | `docs/c4/c4-nivel2-containers.md` |
| 19 | C4 Nível 3 | `docs/c4/c4-nivel3-componentes.md` |
| 20 | C4 Nível 4 | `docs/c4/c4-nivel4-pipeline.md` |
| 21 | Documento Mestre | `docs/master/documento-mestre.md` |
| 22 | Roadmap | `docs/master/roadmap.md` |

Todos os arquivos têm **rodapé com links cruzados** para os documentos relacionados, prontos para referência com `@docs/...` no Continue/Claude.