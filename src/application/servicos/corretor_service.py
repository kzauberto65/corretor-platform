# arquivo: corretor_service.py
from src.persistencia.repositorios.corretor_repository import CorretorRepository

class CorretorService:
    def __init__(self):
        self.repo = CorretorRepository()

    def criar_corretor(self, nome, telefone=None, email=None, creci=None, observacoes=None):
        if not nome or nome.strip() == "":
            raise ValueError("Nome do corretor é obrigatório")

        # Evitar duplicidade por nome
        existente_nome = self.repo.buscar_por_nome(nome)
        if existente_nome:
            # Se telefone também bater, é o mesmo corretor
            if telefone and existente_nome["telefone"] == telefone:
                return existente_nome

        # Evitar duplicidade por e-mail
        if email:
            existente_email = self.repo.buscar_por_email(email)
            if existente_email:
                return existente_email

        # Evitar duplicidade por CRECI
        if creci:
            existente_creci = self.repo.buscar_por_creci(creci)
            if existente_creci:
                return existente_creci

        # Criar corretor
        self.repo.criar(nome, telefone, email, creci, observacoes)

        # Retornar o último inserido
        corretores = self.repo.listar()
        return corretores[-1] if corretores else None

    def listar_corretores(self):
        return self.repo.listar()

    def buscar_por_id(self, corretor_id):
        return self.repo.buscar_por_id(corretor_id)

    def atualizar_corretor(self, corretor_id, nome, telefone=None, email=None, creci=None, observacoes=None):
        existente = self.repo.buscar_por_id(corretor_id)
        if not existente:
            raise ValueError("Corretor não encontrado")

        if not nome or nome.strip() == "":
            raise ValueError("Nome do corretor é obrigatório")

        # Atualizar
        self.repo.atualizar(corretor_id, nome, telefone, email, creci, observacoes)

        return self.repo.buscar_por_id(corretor_id)

    def remover_corretor(self, corretor_id):
        existente = self.repo.buscar_por_id(corretor_id)
        if not existente:
            raise ValueError("Corretor não encontrado")

        self.repo.remover(corretor_id)
        return True