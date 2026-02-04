# arquivo: unidade_repository.py
from src.persistencia.repositorios.base_repository import BaseRepository

class UnidadeRepository(BaseRepository):

    def criar(
        self,
        empreendimento_id,
        construtora_id,
        codigo_unidade,
        metragem,
        valor,
        observacoes=None,
        tipo_unidade_id=None
    ):
        query = """
        INSERT INTO unidades (
            empreendimento_id,
            construtora_id,
            codigo_unidade,
            metragem,
            valor,
            observacoes,
            tipo_unidade_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            query,
            (
                empreendimento_id,
                construtora_id,
                codigo_unidade,
                metragem,
                valor,
                observacoes,
                tipo_unidade_id
            )
        )

    def listar(self):
        return self.fetch_all("SELECT * FROM unidades")

    def listar_completo(self):
        """
        Usa a view vw_unidades_completas para retornar unidades
        já com empreendimento, construtora e tipo.
        """
        return self.fetch_all("SELECT * FROM vw_unidades_completas")

    def buscar_por_id(self, unidade_id):
        return self.fetch_one(
            "SELECT * FROM unidades WHERE id = ?",
            (unidade_id,)
        )

    def listar_por_empreendimento(self, empreendimento_id):
        return self.fetch_all(
            "SELECT * FROM unidades WHERE empreendimento_id = ?",
            (empreendimento_id,)
        )

    def listar_por_construtora(self, construtora_id):
        return self.fetch_all(
            "SELECT * FROM unidades WHERE construtora_id = ?",
            (construtora_id,)
        )

    def atualizar(
        self,
        unidade_id,
        codigo_unidade=None,
        metragem=None,
        valor=None,
        observacoes=None,
        tipo_unidade_id=None
    ):
        query = """
        UPDATE unidades
        SET
            codigo_unidade = ?,
            metragem = ?,
            valor = ?,
            observacoes = ?,
            tipo_unidade_id = ?
        WHERE id = ?
        """
        self.execute(
            query,
            (
                codigo_unidade,
                metragem,
                valor,
                observacoes,
                tipo_unidade_id,
                unidade_id
            )
        )

    def remover(self, unidade_id):
        self.execute(
            "DELETE FROM unidades WHERE id = ?",
            (unidade_id,)
        )