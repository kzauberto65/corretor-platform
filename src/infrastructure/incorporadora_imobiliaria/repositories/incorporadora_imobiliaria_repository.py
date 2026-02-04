import sqlite3
from src.domain.incorporadora_imobiliaria.entities.incorporadora_imobiliaria_entity import IncorporadoraImobiliariaEntity
from src.domain.incorporadora_imobiliaria.dto.incorporadora_imobiliaria_dto import IncorporadoraImobiliariaDTO

class IncorporadoraImobiliariaRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # Cadastrar
    # ---------------------------------------------------------
    def cadastrar(self, entity: IncorporadoraImobiliariaEntity) -> IncorporadoraImobiliariaEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO incorporadora_imobiliaria (
                incorporadora_id,
                imobiliaria_id,
                observacoes
            )
            VALUES (?, ?, ?)
        """, (
            entity.incorporadora_id,
            entity.imobiliaria_id,
            entity.observacoes
        ))

        conn.commit()
        conn.close()
        return entity

    # ---------------------------------------------------------
    # Atualizar
    # ---------------------------------------------------------
    def atualizar(self, entity: IncorporadoraImobiliariaEntity) -> IncorporadoraImobiliariaEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE incorporadora_imobiliaria
            SET observacoes = ?
            WHERE incorporadora_id = ? AND imobiliaria_id = ?
        """, (
            entity.observacoes,
            entity.incorporadora_id,
            entity.imobiliaria_id
        ))

        conn.commit()
        conn.close()
        return entity

    # ---------------------------------------------------------
    # Consultar todos
    # ---------------------------------------------------------
    def consultar(self) -> list[IncorporadoraImobiliariaDTO]:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT incorporadora_id, imobiliaria_id, observacoes
            FROM incorporadora_imobiliaria
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            IncorporadoraImobiliariaDTO(
                incorporadora_id=row[0],
                imobiliaria_id=row[1],
                observacoes=row[2]
            )
            for row in rows
        ]

    # ---------------------------------------------------------
    # Buscar por IDs
    # ---------------------------------------------------------
    def buscar_por_ids(self, incorporadora_id: int, imobiliaria_id: int) -> IncorporadoraImobiliariaDTO | None:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT incorporadora_id, imobiliaria_id, observacoes
            FROM incorporadora_imobiliaria
            WHERE incorporadora_id = ? AND imobiliaria_id = ?
        """, (incorporadora_id, imobiliaria_id))

        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return IncorporadoraImobiliariaDTO(
            incorporadora_id=row[0],
            imobiliaria_id=row[1],
            observacoes=row[2]
        )

    # ---------------------------------------------------------
    # Remover
    # ---------------------------------------------------------
    def remover(self, incorporadora_id: int, imobiliaria_id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM incorporadora_imobiliaria
            WHERE incorporadora_id = ? AND imobiliaria_id = ?
        """, (incorporadora_id, imobiliaria_id))

        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()

        return deleted
