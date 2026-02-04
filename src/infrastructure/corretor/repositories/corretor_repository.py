import sqlite3
from src.domain.corretor.entities.corretor_entity import CorretorEntity

class CorretorRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: CorretorEntity) -> CorretorEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO corretores (
                nome, telefone, email, creci, observacoes
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            entity.nome,
            entity.telefone,
            entity.email,
            entity.creci,
            entity.observacoes
        ))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: CorretorEntity) -> CorretorEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE corretores SET
                nome = ?, telefone = ?, email = ?, creci = ?, observacoes = ?
            WHERE id = ?
        """, (
            entity.nome,
            entity.telefone,
            entity.email,
            entity.creci,
            entity.observacoes,
            entity.id
        ))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[CorretorEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM corretores")
        rows = cur.fetchall()
        conn.close()

        return [
            CorretorEntity(
                id=row[0],
                nome=row[1],
                telefone=row[2],
                email=row[3],
                creci=row[4],
                observacoes=row[5]
            )
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> CorretorEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM corretores WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return CorretorEntity(
            id=row[0],
            nome=row[1],
            telefone=row[2],
            email=row[3],
            creci=row[4],
            observacoes=row[5]
        )

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM corretores WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
