import sqlite3
from src.domain.imobiliaria.dto.imobiliaria_dto import ImobiliariaDTO

class ImobiliariaRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def save(self, dto: ImobiliariaDTO) -> ImobiliariaDTO:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO imobiliarias (nome, cnpj, contato, observacoes)
            VALUES (?, ?, ?, ?)
        """, (dto.nome, dto.cnpj, dto.contato, dto.observacoes))
        dto.id = cur.lastrowid
        conn.commit()
        conn.close()
        return dto

    def update(self, dto: ImobiliariaDTO) -> ImobiliariaDTO:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE imobiliarias SET nome = ?, cnpj = ?, contato = ?, observacoes = ?
            WHERE id = ?
        """, (dto.nome, dto.cnpj, dto.contato, dto.observacoes, dto.id))
        conn.commit()
        conn.close()
        return dto

    def find(self):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM imobiliarias")
        rows = cur.fetchall()
        conn.close()
        return [ImobiliariaDTO(*r) for r in rows]

    def find_by_id(self, id: int):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM imobiliarias WHERE id = ?", (id,))
        r = cur.fetchone()
        conn.close()
        return ImobiliariaDTO(*r) if r else None

    def delete(self, id: int):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM imobiliarias WHERE id = ?", (id,))
        conn.commit()
        conn.close()
