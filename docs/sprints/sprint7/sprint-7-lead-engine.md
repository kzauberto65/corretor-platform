
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