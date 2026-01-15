from src.persistencia.repositorios.base_repository import BaseRepository

class ConstrutoraImobiliariaRepository(BaseRepository):

    def criar(self, construtora_id, imobiliaria_id):
        query = """
        INSERT INTO construtora_imobiliaria (construtora_id, imobiliaria_id)
        VALUES (?, ?)
        """
        self.execute(query, (construtora_id, imobiliaria_id))

    def listar(self):
        return self.fetch_all("SELECT * FROM construtora_imobiliaria")

    def listar_por_construtora(self, construtora_id):
        return self.fetch_all(
            "SELECT * FROM construtora_imobiliaria WHERE construtora_id = ?",
            (construtora_id,)
        )

    def listar_por_imobiliaria(self, imobiliaria_id):
        return self.fetch_all(
            "SELECT * FROM construtora_imobiliaria WHERE imobiliaria_id = ?",
            (imobiliaria_id,)
        )