# arquivo: construtora_service.py
from src.persistencia.repositorios.construtora_repository import ConstrutoraRepository

class ConstrutoraService:
    def __init__(self):
        self.repo = ConstrutoraRepository()

    def criar_construtora(self, nome, cnpj=None, contato=None, observacoes=None):
        if not nome or nome.strip() == "":
            raise ValueError("Nome da construtora é obrigatório")

        # Evitar duplicidade por nome
        existente_nome = self.repo.buscar_por_nome(nome)
        if existente_nome:
            return existente_nome

        # Evitar duplicidade por CNPJ (quando informado)
        if cnpj:
            existentes = self.repo.listar()
            for c in existentes:
                if c["cnpj"] and c["cnpj"] == cnpj:
                    return c

        # Criar construtora
        self.repo.criar(nome, cnpj, contato, observacoes)

        # Retornar a última inserida
        construtoras = self.repo.listar()
        return construtoras[-1] if construtoras else None

    def listar_construtoras(self):
        return self.repo.listar()

    def buscar_por_id(self, construtora_id):
        return self.repo.buscar_por_id(construtora_id)

    def atualizar_construtora(self, construtora_id, nome, cnpj=None, contato=None, observacoes=None):
        existente = self.repo.buscar_por_id(construtora_id)
        if not existente:
            raise ValueError("Construtora não encontrada")

        if not nome or nome.strip() == "":
            raise ValueError("Nome da construtora é obrigatório")

        # Atualizar
        self.repo.atualizar(construtora_id, nome, cnpj, contato, observacoes)

        return self.repo.buscar_por_id(construtora_id)

    def remover_construtora(self, construtora_id):
        existente = self.repo.buscar_por_id(construtora_id)
        if not existente:
            raise ValueError("Construtora não encontrada")

        self.repo.remover(construtora_id)
        return True