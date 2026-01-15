from src.persistencia.repositorios.base_repository import BaseRepository

class ImovelRepository(BaseRepository):

    def criar(
        self,
        regiao,
        bairro,
        cidade,
        estado,
        produto,
        endereco=None,
        data_entrega=None,
        status_entrega=None,
        tipo=None,
        descricao=None
    ):
        query = """
        INSERT INTO imoveis (
            regiao, bairro, cidade, estado, produto,
            endereco, data_entrega, status_entrega, tipo, descricao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            query,
            (
                regiao, bairro, cidade, estado, produto,
                endereco, data_entrega, status_entrega, tipo, descricao
            )
        )

    def listar(self):
        return self.fetch_all("SELECT * FROM imoveis")

    def buscar_por_id(self, id):
        return self.fetch_one("SELECT * FROM imoveis WHERE id = ?", (id,))