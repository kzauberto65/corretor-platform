
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