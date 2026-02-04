from dataclasses import dataclass

@dataclass
class ImobiliariaEntity:
    id: int | None
    nome: str | None
    cnpj: str | None
    contato: str | None
    observacoes: str | None

    def to_dict(self):
        return self.__dict__
