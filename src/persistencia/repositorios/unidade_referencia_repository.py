from src.persistencia.repositorios.base_repository import BaseRepository

class UnidadeReferenciaRepository(BaseRepository):

    def criar_ou_obter(self, codigo):
        # 1. Buscar existente
        existente = self.fetch_one(
            "SELECT * FROM unidade_referencia WHERE LOWER(codigo) = LOWER(?)",
            (codigo,)
        )

        if existente:
            return existente

        # 2. Criar nova
        self.execute(
            "INSERT INTO unidade_referencia (codigo) VALUES (?)",
            (codigo,)
        )

        # 3. Retornar recém-criada
        return self.fetch_one(
            "SELECT * FROM unidade_referencia WHERE LOWER(codigo) = LOWER(?)",
            (codigo,)
        )

    def listar(self):
        return self.fetch_all("SELECT * FROM unidade_referencia")

    def buscar_por_id(self, unidade_id):
        return self.fetch_one(
            "SELECT * FROM unidade_referencia WHERE id = ?",
            (unidade_id,)
        )

    def remover(self, unidade_id):
        self.execute(
            "DELETE FROM unidade_referencia WHERE id = ?",
            (unidade_id,)
        )