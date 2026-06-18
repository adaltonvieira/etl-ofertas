import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()   # carrega as variaveis do arquivo .env


def get_connection():
    """Abre uma conexao com o PostgreSQL."""
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        dbname=os.environ.get("DB_NAME", "etl_ofertas"),
        user=os.environ.get("DB_USER", "adalton"),
        password=os.environ["DB_PASSWORD"],
        row_factory=dict_row,
    )


def init_db():
    """Cria a tabela e o indice, se ainda nao existirem."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS precos (
                id          SERIAL PRIMARY KEY,
                produto     TEXT NOT NULL,
                preco       DOUBLE PRECISION NOT NULL,
                moeda       TEXT NOT NULL DEFAULT 'BRL',
                coletado_em TIMESTAMP NOT NULL
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_precos_produto_data
            ON precos (produto, coletado_em);
        """)
    conn.commit()
    conn.close()
    print("Tabela 'precos' pronta no PostgreSQL.")


if __name__ == "__main__":
    init_db()
