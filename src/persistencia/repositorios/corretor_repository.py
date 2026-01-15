from src.persistencia.repositorios.base_repository import BaseRepository

class CorretorRepository(BaseRepository):

    def criar(self, nome, telefone=None, email=None, creci=None, observacoes=None):
        query = """
        INSERT INTO corretores (nome, telefone, email, creci, observacoes)
        VALUES (?, ?, ?, ?, ?)
        """
        self.execute(query, (nome, telefone, email, creci, observacoes))

    def listar(self):
        return self.fetch_all("SELECT * FROM corretores")

    def buscar_por_id(self, id):
        return self.fetch_one("SELECT * FROM corretores WHERE id = ?", (id,))