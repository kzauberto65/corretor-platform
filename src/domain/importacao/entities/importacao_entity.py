from dataclasses import dataclass

@dataclass
class ImportacaoEntity:
    id: int | None
    tipo: str | None
    arquivo: str | None
    origem: str | None
    total_registros: int | None
    status: str | None
    data_execucao: str | None
    sucesso: int | None
    erros: int | None
    log: str | None
