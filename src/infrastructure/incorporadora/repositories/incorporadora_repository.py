import sqlite3
from src.domain.incorporadora.entities.incorporadora_entity import IncorporadoraEntity

class IncorporadoraRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: IncorporadoraEntity) -> IncorporadoraEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO incorporadora (
                nome, cnpj, reputacao, historico_obra
            )
            VALUES (?, ?, ?, ?)
        """, (
            entity.nome,
            entity.cnpj,
            entity.reputacao,
            entity.historico_obra
        ))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: IncorporadoraEntity) -> IncorporadoraEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE incorporadora SET
                nome = ?, cnpj = ?, reputacao = ?, historico_obra = ?
            WHERE id = ?
        """, (
            entity.nome,
            entity.cnpj,
            entity.reputacao,
            entity.historico_obra,
            entity.id
        ))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[IncorporadoraEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM incorporadora")
        rows = cur.fetchall()
        conn.close()

        return [
            IncorporadoraEntity(
                id=row[0],
                nome=row[1],
                cnpj=row[2],
                reputacao=row[3],
                historico_obra=row[4]
            )
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> IncorporadoraEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM incorporadora WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return IncorporadoraEntity(
            id=row[0],
            nome=row[1],
            cnpj=row[2],
            reputacao=row[3],
            historico_obra=row[4]
        )

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM incorporadora WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
