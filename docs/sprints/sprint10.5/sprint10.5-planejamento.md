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

Pipeline Alvo

Lead + Unidades → IAEngine (vetores + similaridade + conversão) → DTO → IARepository → SQLite
Resultado Esperado
☐ Modelo de dados correto
☐ Unidades reais por empreendimento
☐ Vetorização consistente
☐ Matching granular
☐ IA preparada para embeddings
☐ Pipeline pronto para Sprint 11
📌 Rodapé: Decisão arquitetural: ADR-002.
Schema alvo: Schema Alvo 10.5.
