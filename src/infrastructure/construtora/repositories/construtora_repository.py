import sqlite3
from src.domain.construtora.entities.construtora_entity import ConstrutoraEntity

class ConstrutoraRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: ConstrutoraEntity) -> ConstrutoraEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO construtoras (
                nome, cnpj, contato, observacoes, fonte,
                data_registro, usuario_id, justificativa
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entity.nome,
            entity.cnpj,
            entity.contato,
            entity.observacoes,
            entity.fonte,
            entity.data_registro,
            entity.usuario_id,
            entity.justificativa
        ))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: ConstrutoraEntity) -> ConstrutoraEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE construtoras SET
                nome = ?, cnpj = ?, contato = ?, observacoes = ?, fonte = ?,
                data_registro = ?, usuario_id = ?, justificativa = ?
            WHERE id = ?
        """, (
            entity.nome,
            entity.cnpj,
            entity.contato,
            entity.observacoes,
            entity.fonte,
            entity.data_registro,
            entity.usuario_id,
            entity.justificativa,
            entity.id
        ))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[ConstrutoraEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM construtoras")
        rows = cur.fetchall()
        conn.close()

        return [
            ConstrutoraEntity(
                id=row[0],
                nome=row[1],
                cnpj=row[2],
                contato=row[3],
                observacoes=row[4],
                fonte=row[5],
                data_registro=row[6],
                usuario_id=row[7],
                justificativa=row[8]
            )
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> ConstrutoraEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM construtoras WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return ConstrutoraEntity(
            id=row[0],
            nome=row[1],
            cnpj=row[2],
            contato=row[3],
            observacoes=row[4],
            fonte=row[5],
            data_registro=row[6],
            usuario_id=row[7],
            justificativa=row[8]
        )

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM construtoras WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
