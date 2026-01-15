# src/persistencia/repositorios/base_repository.py
import sqlite3
from pathlib import Path
from src.parsing import get_project_root

ROOT = get_project_root()
DB_PATH = ROOT / "database" / "corretor.db"

class BaseRepository:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query, params=()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        return cur

    def fetch_all(self, query, params=()):
        cur = self.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

    def fetch_one(self, query, params=()):
        cur = self.execute(query, params)
        row = cur.fetchone()
        return dict(row) if row else None