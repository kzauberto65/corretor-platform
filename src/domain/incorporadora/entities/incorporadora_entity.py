# ============================================================
# ENTITY: IncorporadoraEntity
# Camada: domain/incorporadora/entities/
# Descrição: Representa incorporadora persistida no banco.
# Sprint: 10.5
# ============================================================

from dataclasses import dataclass, asdict

@dataclass
class IncorporadoraEntity:
    id: int | None = None
    nome: str | None = None
    cnpj: str | None = None
    reputacao: int | None = None
    historico_obra: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)