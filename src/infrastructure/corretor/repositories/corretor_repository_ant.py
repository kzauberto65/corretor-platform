# arquivo: corretor_repository.py
from src.persistencia.repositorios.base_repository import BaseRepository

class CorretorRepository(BaseRepository):

    def criar(self, nome, telefone=None, email=None, creci=None, observacoes=None):
        query = """
        INSERT INTO corretores (
            nome,
            telefone,
            email,
            creci,
            observacoes
        )
        VALUES (?, ?, ?, ?, ?)
        """
        self.execute(query, (nome, telefone, email, creci, observacoes))

    def listar(self):
        return self.fetch_all("SELECT * FROM corretores")

    def buscar_por_id(self, corretor_id):
        return self.fetch_one(
            "SELECT * FROM corretores WHERE id = ?",
            (corretor_id,)
        )

    def buscar_por_nome(self, nome):
        return self.fetch_one(
            "SELECT * FROM corretores WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )

    def buscar_por_email(self, email):
        return self.fetch_one(
            "SELECT * FROM corretores WHERE LOWER(email) = LOWER(?)",
            (email,)
        )

    def buscar_por_creci(self, creci):
        return self.fetch_one(
            "SELECT * FROM corretores WHERE creci = ?",
            (creci,)
        )

    def atualizar(self, corretor_id, nome, telefone=None, email=None, creci=None, observacoes=None):
        query = """
        UPDATE corretores
        SET
            nome = ?,
            telefone = ?,
            email = ?,
            creci = ?,
            observacoes = ?
        WHERE id = ?
        """
        self.execute(
            query,
            (nome, telefone, email, creci, observacoes, corretor_id)
        )

    def remover(self, corretor_id):
        self.execute(
            "DELETE FROM corretores WHERE id = ?",
            (corretor_id,)
        )