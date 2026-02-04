from dataclasses import dataclass

@dataclass
class ImportacaoInputDTO:
    tipo: str | None
    arquivo: str | None
    origem: str | None
    total_registros: int | None
    status: str | None
    data_execucao: str | None
    sucesso: int | None
    erros: int | None
    log: str | None
