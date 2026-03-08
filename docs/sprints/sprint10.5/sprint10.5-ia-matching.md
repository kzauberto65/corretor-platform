
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