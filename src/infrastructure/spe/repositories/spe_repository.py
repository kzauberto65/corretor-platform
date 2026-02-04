import sqlite3
from src.domain.spe.entities.spe_entity import SPEEntity

class SPERepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: SPEEntity) -> SPEEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO spe (
                nome, cnpj, observacoes
            )
            VALUES (?, ?, ?)
        """, (
            entity.nome,
            entity.cnpj,
            entity.observacoes
        ))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: SPEEntity) -> SPEEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE spe SET
                nome = ?, cnpj = ?, observacoes = ?
            WHERE id = ?
        """, (
            entity.nome,
            entity.cnpj,
            entity.observacoes,
            entity.id
        ))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[SPEEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM spe")
        rows = cur.fetchall()
        conn.close()

        return [
            SPEEntity(
                id=row[0],
                nome=row[1],
                cnpj=row[2],
                observacoes=row[3]
            )
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> SPEEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM spe WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return SPEEntity(
            id=row[0],
            nome=row[1],
            cnpj=row[2],
            observacoes=row[3]
        )

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM spe WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
