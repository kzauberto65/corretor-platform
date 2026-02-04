import sqlite3
from src.domain.unidade.entities.unidade_entity import UnidadeEntity

class UnidadeRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def cadastrar(self, entity: UnidadeEntity) -> UnidadeEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
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
        """, (
            entity.empreendimento_id,
            entity.construtora_id,
            entity.codigo_unidade,
            entity.metragem,
            entity.valor,
            entity.observacoes,
            entity.tipo_unidade_id
        ))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: UnidadeEntity) -> UnidadeEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE unidades SET
                empreendimento_id = ?,
                construtora_id = ?,
                codigo_unidade = ?,
                metragem = ?,
                valor = ?,
                observacoes = ?,
                tipo_unidade_id = ?
            WHERE id = ?
        """, (
            entity.empreendimento_id,
            entity.construtora_id,
            entity.codigo_unidade,
            entity.metragem,
            entity.valor,
            entity.observacoes,
            entity.tipo_unidade_id,
            entity.id
        ))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[UnidadeEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM unidades")
        rows = cur.fetchall()
        conn.close()

        return [
            UnidadeEntity(
                id=row[0],
                empreendimento_id=row[1],
                construtora_id=row[2],
                codigo_unidade=row[3],
                metragem=row[4],
                valor=row[5],
                observacoes=row[6],
                tipo_unidade_id=row[7]
            )
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> UnidadeEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM unidades WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return UnidadeEntity(
            id=row[0],
            empreendimento_id=row[1],
            construtora_id=row[2],
            codigo_unidade=row[3],
            metragem=row[4],
            valor=row[5],
            observacoes=row[6],
            tipo_unidade_id=row[7]
        )

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM unidades WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
