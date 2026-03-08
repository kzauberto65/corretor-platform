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