# ADR-005 - Modelo de Financiamento por Unidade (Unidade ↔ Financiamento Satélite)

Status: Proposto
Autor: Equipe Auto Router
Data: 2026-03-08
Local: docs/adr/adr-005-modelo-financiamento-unidade.md

---

## Contexto

- O modelo atual do ADR-005 não deixou explícita a cardinalidade entre Unidade e Financiamento Satélite.
- Requisitos atuais (mantidos do contrato): a Unidade pode ter zero ou um financiamento satélite; não deve haver múltiplos financiamentos por unidade.
- Objetivo: formalizar o relacionamento 1:1 entre Unidade e Financiamento Satélite, com a referência mantida via FK na tabela de Financiamento para Unidade.

## Decisão

1. Relacionamento 1:1 entre Unidade e Financiamento Satélite:
   - Uma Unidade pode ter zero ou um financiamento satélite.
   - A referência fica no modelo de dados via FK: `tabelas_financiamento.unidade_id` deve ser único (uniqueness) para garantir 1:1.
2. Abstração no domínio:
   - A Unidade deve refletir esse relacionamento por meio de um atributo opcional (padrão: vazio/null) que aponta para o Financiamento associado, quando existir.
3. Sem APIs no curto prazo:
   - Mantemos o enfoque apenas no domínio, aplicação e infraestrutura já definidos pelo ADR-005, sem introduzir APIs.

## Consequências

- Banco de dados: adicionar unicidade em `unidade_id` na tabela `tabelas_financiamento` (para garantir 1:1).
- Domínio: a entidade `Unidade` passa a incluir um relacionamento 1:1 com `TabelaFinanciamento` (opcional).
- Repositórios: o método de busca por unidade passa a retornar um único `TabelaFinanciamento` (ou None) em vez de uma lista.
- Migration: se houver dados existentes com múltiplos financiamentos por unidade, será necessária uma migração para consolidar para zero ou um financiamento por unidade.

## Observações

- Este ADR foca apenas no modelo conceitual e no impacto estrutural (DB e domínio); não altera a API.
- Caso haja dados existentes com múltiplos financiamentos por unidade, planejar migração para manter apenas um financiamento por unidade (definindo regra de seleção).