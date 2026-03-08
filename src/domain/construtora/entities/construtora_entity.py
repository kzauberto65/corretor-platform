# ============================================================
# ENTITY: ConstrutoraEntity
# Camada: domain/construtora/entities/
# Descrição: Representa uma construtora já persistida no banco.
#            É o objeto de domínio completo — tem identidade (id).
#            Construtora = empresa responsável pela obra física.
#            Pode ser referenciada como proprietario_id em
#            empreendimentos (FK → construtoras).
#            Usado pelo Repository para mapear rows do SQLite.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass, asdict

@dataclass
class ConstrutoraEntity:
    # Identidade no banco — nunca None após persistido
    id: int | None = None

    # Identificação principal
    nome: str | None = None              # razão social ou nome fantasia
    cnpj: str | None = None              # CNPJ formatado ou somente dígitos

    # Contato
    contato: str | None = None           # telefone, e-mail ou nome do responsável

    # Observações e rastreabilidade
    observacoes: str | None = None       # notas livres sobre a construtora
    fonte: str | None = None             # origem do cadastro: planilha, CRM, manual
    data_registro: str | None = None     # formato ISO: YYYY-MM-DD
    usuario_id: str | None = None        # quem cadastrou (ref. futura a usuários)
    justificativa: str | None = None     # motivo de inclusão/alteração

    # ----------------------------------------------------------
    # MÉTODOS DE DOMÍNIO
    # ----------------------------------------------------------

    def resumo(self) -> str:
        """Retorna linha de resumo da construtora para CLI e futuras UIs.
        Ex: 'MRV Engenharia | CNPJ: 08.343.492/0001-20'"""
        partes = [p for p in [self.nome, f"CNPJ: {self.cnpj}" if self.cnpj else None] if p]
        return " | ".join(partes) if partes else f"Construtora #{self.id}"

    def to_dict(self) -> dict:
        """Serializa a entity para dict.
        Usa dataclasses.asdict — mais seguro que __dict__ para objetos aninhados."""
        return asdict(self)