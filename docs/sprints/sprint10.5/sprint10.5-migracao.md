
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

3. Criar tabela unidade_referencia
Executar SQL de criação (ver Schema)
4. Atualizar unidade_referencia para apontar para unidades reais
5. Atualizar IA e Matching para operar por unidade
Ver IA + Matching
6. Manter compatibilidade com CLI atual
Validações pós-migração
Cada empreendimento deve ter pelo menos 1 unidade
unidade_referencia_id deve ser válido
Disponibilidade deve ser consistente
Vetores devem ser regenerados
📌 Rodapé: Schema completo: Schema Alvo 10.5.
Testes: Sprint 10.5 — CLI + Testes.