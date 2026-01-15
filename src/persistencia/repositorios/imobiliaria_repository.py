from src.persistencia.repositorios.base_repository import BaseRepository

class ImobiliariaRepository(BaseRepository):

    def criar(self, nome, cnpj=None, contato=None, observacoes=None):
        query = """
        INSERT INTO imobiliarias (nome, cnpj, contato, observacoes)
        VALUES (?, ?, ?, ?)
        """
        self.execute(query, (nome, cnpj, contato, observacoes))

    def listar(self):
        return self.fetch_all("SELECT * FROM imobiliarias")

    def buscar_por_id(self, id):
        return self.fetch_one("SELECT * FROM imobiliarias WHERE id = ?", (id,))