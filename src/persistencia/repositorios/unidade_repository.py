from src.persistencia.repositorios.base_repository import BaseRepository

class UnidadeRepository(BaseRepository):

    def criar(
        self,
        imovel_id,
        construtora_id,
        codigo_unidade,
        metragem,
        valor,
        observacoes=None,
        unidade_referencia_id=None
    ):
        query = """
        INSERT INTO unidades (
            imovel_id,
            construtora_id,
            codigo_unidade,
            metragem,
            valor,
            observacoes,
            unidade_referencia_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            query,
            (
                imovel_id,
                construtora_id,
                codigo_unidade,
                metragem,
                valor,
                observacoes,
                unidade_referencia_id
            )
        )

    def listar(self):
        return self.fetch_all("SELECT * FROM unidades")

    def listar_por_imovel(self, imovel_id):
        return self.fetch_all(
            "SELECT * FROM unidades WHERE imovel_id = ?",
            (imovel_id,)
        )

    def listar_por_construtora(self, construtora_id):
        return self.fetch_all(
            "SELECT * FROM unidades WHERE construtora_id = ?",
            (construtora_id,)
        )