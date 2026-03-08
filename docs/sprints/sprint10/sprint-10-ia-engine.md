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

Resultado Final
☑ IA Engine implementado
☑ Vetorização numérica funcional
☑ Similaridade vetorial
☑ Previsão de conversão
☑ Reasons explicáveis
☑ Persistência completa
☑ CLI operacional
☑ Correções críticas aplicadas
☑ Ranking validado com lead real
☑ Sprint concluída com sucesso
📌 Rodapé: Problemas encontrados e correções em
Sprint 10 — Problemas e Correções.
ADR do motor: ADR-003.