import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "precos.db"


def get_connection():
    """Abre uma conexão com o banco SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria a tabela e o índice, se ainda não existirem."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS precos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            produto     TEXT    NOT NULL,
            preco       REAL    NOT NULL,
            moeda       TEXT    NOT NULL DEFAULT 'BRL',
            coletado_em TEXT    NOT NULL
        );
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_precos_produto_data
        ON precos (produto, coletado_em);
    """)
    conn.commit()
    conn.close()
    print(f"Banco pronto em: {DB_PATH}")


if __name__ == "__main__":
    init_db()
