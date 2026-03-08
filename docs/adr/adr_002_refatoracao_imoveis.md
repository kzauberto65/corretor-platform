
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