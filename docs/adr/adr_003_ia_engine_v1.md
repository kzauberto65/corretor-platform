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

Pipeline

Lead + Imóveis → IAEngine → IAInputDTO → IARepository → SQLite
Limitações conhecidas (v1)
Não utiliza embeddings textuais
Não interpreta descrição do imóvel
Não interpreta profile_json
Similaridade baixa para vetores de magnitude muito diferente
Dependência da estrutura atual de empreendimentos
Evolução prevista (Sprint 11)
Embeddings reais
Vetorização semântica
Pesos dinâmicos
Aprendizado contínuo
📌 Rodapé: Problemas e correções detalhados em
Sprint 10 — Problemas e Correções.
Evolução planejada em
Sprint 10.5 — IA + Matching.


