import sqlite3
from src.domain.unidade_referencia.entities.unidade_referencia_entity import UnidadeReferenciaEntity

class UnidadeReferenciaRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: UnidadeReferenciaEntity) -> UnidadeReferenciaEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO unidade_referencia (codigo)
            VALUES (?)
        """, (entity.codigo,))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: UnidadeReferenciaEntity) -> UnidadeReferenciaEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE unidade_referencia SET
                codigo = ?
            WHERE id = ?
        """, (entity.codigo, entity.id))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[UnidadeReferenciaEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM unidade_referencia")
        rows = cur.fetchall()
        conn.close()

        return [
            UnidadeReferenciaEntity(id=row[0], codigo=row[1])
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> UnidadeReferenciaEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM unidade_referencia WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return UnidadeReferenciaEntity(id=row[0], codigo=row[1])

    def buscar_por_codigo(self, codigo: str) -> UnidadeReferenciaEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM unidade_referencia WHERE codigo = ?", (codigo,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return UnidadeReferenciaEntity(id=row[0], codigo=row[1])

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM unidade_referencia WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
