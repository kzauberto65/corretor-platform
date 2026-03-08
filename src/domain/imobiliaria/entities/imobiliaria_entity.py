# ============================================================
# ENTITY: ImobiliariaEntity
# Camada: domain/imobiliaria/entities/
# Descrição: Representa imobiliária persistida no banco.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass, asdict

@dataclass
class ImobiliariaEntity:
    id: int | None = None
    nome: str | None = None
    cnpj: str | None = None
    contato: str | None = None
    observacoes: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)