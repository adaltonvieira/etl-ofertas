from datetime import datetime
from db import get_connection


def carregar_precos(itens):
    """Grava uma lista de itens no banco, com carimbo de data/hora."""
    agora = datetime.now().replace(microsecond=0)
    conn = get_connection()
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO precos (produto, preco, moeda, coletado_em)
            VALUES (%s, %s, %s, %s)
            """,
            [(i["produto"], i["preco"], i["moeda"], agora) for i in itens],
        )
    conn.commit()
    conn.close()
    print(f"{len(itens)} registros gravados em {agora}")
