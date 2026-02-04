import sqlite3
from src.domain.importacao.entities.importacao_entity import ImportacaoEntity

class ImportacaoRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: ImportacaoEntity) -> ImportacaoEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO importacoes (
                tipo, arquivo, origem, total_registros, status,
                data_execucao, sucesso, erros, log
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entity.tipo,
            entity.arquivo,
            entity.origem,
            entity.total_registros,
            entity.status,
            entity.data_execucao,
            entity.sucesso,
            entity.erros,
            entity.log
        ))
        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: ImportacaoEntity) -> ImportacaoEntity:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE importacoes SET
                tipo = ?, arquivo = ?, origem = ?, total_registros = ?,
                status = ?, data_execucao = ?, sucesso = ?, erros = ?, log = ?
            WHERE id = ?
        """, (
            entity.tipo,
            entity.arquivo,
            entity.origem,
            entity.total_registros,
            entity.status,
            entity.data_execucao,
            entity.sucesso,
            entity.erros,
            entity.log,
            entity.id
        ))
        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[ImportacaoEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM importacoes")
        rows = cur.fetchall()
        conn.close()

        return [
            ImportacaoEntity(
                id=row[0],
                tipo=row[1],
                arquivo=row[2],
                origem=row[3],
                total_registros=row[4],
                status=row[5],
                data_execucao=row[6],
                sucesso=row[7],
                erros=row[8],
                log=row[9]
            )
            for row in rows
        ]

    def buscar_por_id(self, id: int) -> ImportacaoEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM importacoes WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return ImportacaoEntity(
            id=row[0],
            tipo=row[1],
            arquivo=row[2],
            origem=row[3],
            total_registros=row[4],
            status=row[5],
            data_execucao=row[6],
            sucesso=row[7],
            erros=row[8],
            log=row[9]
        )

    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM importacoes WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
