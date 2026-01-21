# arquivo: construtora_repository.py
from src.persistencia.repositorios.base_repository import BaseRepository

class ConstrutoraRepository(BaseRepository):

    def criar(self, nome, cnpj=None, contato=None, observacoes=None):
        query = """
        INSERT INTO construtoras (
            nome,
            cnpj,
            contato,
            observacoes
        )
        VALUES (?, ?, ?, ?)
        """
        self.execute(query, (nome, cnpj, contato, observacoes))

    def listar(self):
        return self.fetch_all("SELECT * FROM construtoras")

    def buscar_por_id(self, construtora_id):
        return self.fetch_one(
            "SELECT * FROM construtoras WHERE id = ?",
            (construtora_id,)
        )

    def buscar_por_nome(self, nome):
        return self.fetch_one(
            "SELECT * FROM construtoras WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )

    def atualizar(self, construtora_id, nome, cnpj=None, contato=None, observacoes=None):
        query = """
        UPDATE construtoras
        SET
            nome = ?,
            cnpj = ?,
            contato = ?,
            observacoes = ?
        WHERE id = ?
        """
        self.execute(
            query,
            (nome, cnpj, contato, observacoes, construtora_id)
        )

    def remover(self, construtora_id):
        self.execute(
            "DELETE FROM construtoras WHERE id = ?",
            (construtora_id,)
        )