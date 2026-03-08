# Sprint 10.5 — CLI e Testes

---

## Novos Comandos CLI

```text
unidade add       → Adicionar unidade a um empreendimento
unidade list      → Listar unidades (com filtros)
unidade update    → Atualizar unidade
unidade delete    → Remover unidade

Ajustes em Comandos Existentes

matching run          → matching run-unidades
ia run                → ia run-unidades
Testes Obrigatórios
Testes mínimos
 Criação de unidades
 Migração de dados (empreendimento → unidade padrão)
 Matching por unidade
 IA por unidade
 reasons_json atualizado com dados da unidade
 CLI completo (add, list, update, delete)
 Integridade no SQLite
Validações
 unidade_referencia_id válido
 Unidade pertence ao empreendimento correto
 Disponibilidade consistente (disponível/vendido/reservado)
 Vetores gerados corretamente após migração
📌 Rodapé: Schema das tabelas: Sprint 10.5 — Schema.
Migração: Sprint 10.5 — Migração.
Contrato de arquitetura: ADR-001.