
---

## `docs/sprints/sprint10.5/sprint-10-5-repositorios.md`

```markdown
# Sprint 10.5 — Repositórios

---

## UnidadeRepository (novo)

Local: `src/infrastructure/unidade/repositories/unidade_repository.py`

### Métodos

```python
class UnidadeRepository:
    def save(self, dto) -> int: ...
    def update(self, id, dto) -> None: ...
    def delete(self, id) -> None: ...
    def list_all(self) -> list: ...
    def list_by_empreendimento(self, empreendimento_id) -> list: ...
    def list_disponiveis(self) -> list: ...

EmpreendimentoRepository (atualizado)
Local: src/infrastructure/empreendimento/repositories/empreendimento_repository.py

Novos métodos

class EmpreendimentoRepository:
    # métodos existentes mantidos
    def list_unidades_by_empreendimento(self, id) -> list: ...
    def list_unidades_disponiveis(self) -> list: ...
    def get_unidade_referencia(self, empreendimento_id) -> dict: ...
Regras (conforme ADR-001)
Apenas CRUD
Sem regra de negócio
Implementa interface do domain
📌 Rodapé: Contrato de arquitetura: ADR-001.
Schema das tabelas: Sprint 10.5 — Schema.