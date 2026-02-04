import sqlite3

def test_debug_local():
    conn = sqlite3.connect("corretor.db")
    print("BANCO:", conn.execute("PRAGMA database_list").fetchall())
