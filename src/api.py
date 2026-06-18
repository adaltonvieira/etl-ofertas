from fastapi import FastAPI
from db import get_connection

app = FastAPI(title="ETL de Ofertas API")


@app.get("/")
def raiz():
    return {"mensagem": "API do ETL de Ofertas. Acesse /docs para a documentacao."}


@app.get("/precos")
def listar_precos(produto: str | None = None, limite: int = 50):
    """Lista as coletas mais recentes, opcionalmente filtrando por produto."""
    conn = get_connection()
    if produto:
        linhas = conn.execute(
            "SELECT * FROM precos WHERE produto ILIKE %s "
            "ORDER BY coletado_em DESC LIMIT %s",
            (f"%{produto}%", limite),
        ).fetchall()
    else:
        linhas = conn.execute(
            "SELECT * FROM precos ORDER BY coletado_em DESC LIMIT %s",
            (limite,),
        ).fetchall()
    conn.close()
    return linhas


@app.get("/precos/variacao")
def variacao():
    """Variacao de preco entre cada coleta e a anterior (window function)."""
    conn = get_connection()
    linhas = conn.execute("""
        SELECT produto, coletado_em, preco,
               ROUND((preco - LAG(preco) OVER (
                   PARTITION BY produto ORDER BY coletado_em))::numeric, 4) AS variacao
        FROM precos
        ORDER BY produto, coletado_em
    """).fetchall()
    conn.close()
    return linhas
