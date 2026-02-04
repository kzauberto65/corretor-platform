import sqlite3
from src.domain.unidade_referencia_tipo.entities.unidade_referencia_tipo_entity import UnidadeReferenciaTipoEntity

class UnidadeReferenciaTipoRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: UnidadeReferenciaTipoEntity) -> UnidadeReferenciaTipoEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO unidade_referencia_tipo (
                nome
            )
            VALUES (?)
        """, (entity.nome,))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: UnidadeReferenciaTipoEntity) -> UnidadeReferenciaTipoEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE unidade_referencia_tipo SET
                nome = ?
            WHERE id = ?
        """, (
            entity.nome,
            entity.id
        ))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[UnidadeReferenciaTipoEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM unidade_referencia_tipo")
        rows = cur.fetchall()
        conn.close()

        return [
            UnidadeReferenciaTipoEntity(
                id=row[0],
                nome=row[1]
            )
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> UnidadeReferenciaTipoEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM unidade_referencia_tipo WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return UnidadeReferenciaTipoEntity(
            id=row[0],
            nome=row[1]
        )

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM unidade_referencia_tipo WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
