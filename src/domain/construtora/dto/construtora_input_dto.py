from dataclasses import dataclass

@dataclass
class ConstrutoraInputDTO:
    nome: str | None
    cnpj: str | None
    contato: str | None
    observacoes: str | None
    fonte: str | None
    data_registro: str | None
    usuario_id: str | None
    justificativa: str | None
