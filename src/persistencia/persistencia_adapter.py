import sqlite3
from pathlib import Path
from parsing import get_project_root

ROOT = get_project_root()
DB_PATH = ROOT / "database" / "corretor.db"

class PersistenciaAdapter:

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def registrar_importacao(self, dados):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO importacoes (tipo, arquivo, origem, total_registros, status, data_execucao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                dados["tipo"],
                dados["arquivo"],
                dados["origem"],
                dados["total_registros"],
                dados["status"],
                dados["data_execucao"]
            ))
            conn.commit()
            return cursor.lastrowid

    def atualizar_importacao(self, id_importacao, sucesso, erros, log):
        with self._connect() as conn:
            conn.execute("""
                UPDATE importacoes
                SET sucesso = ?, erros = ?, log = ?, status = 'finalizado'
                WHERE id = ?
            """, (sucesso, erros, log, id_importacao))
            conn.commit()

    def salvar_imovel(self, dados):
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO imoveis (endereco, cidade, estado, preco, proprietario_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                dados["endereco"],
                dados["cidade"],
                dados["estado"],
                dados["preco"],
                dados["proprietario_id"]
            ))
            conn.commit()