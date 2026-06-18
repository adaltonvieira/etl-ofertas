from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use("Agg")   # gera imagem sem precisar de tela/janela
import matplotlib.pyplot as plt
from db import get_connection

CHARTS_DIR = Path(__file__).resolve().parent.parent / "charts"


def relatorio_texto():
    conn = get_connection()
    linhas = conn.execute("""
        SELECT produto,
               COUNT(*)             AS coletas,
               MIN(preco)           AS minimo,
               MAX(preco)           AS maximo,
               ROUND(AVG(preco), 4) AS media
        FROM precos
        GROUP BY produto
    """).fetchall()
    conn.close()
    print("\n=== Relatório de preços ===")
    for r in linhas:
        print(f"{r['produto']}: {r['coletas']} coletas | "
              f"min {r['minimo']} | max {r['maximo']} | média {r['media']}")


def grafico_variacao():
    conn = get_connection()
    linhas = conn.execute("""
        SELECT produto, coletado_em, preco
        FROM precos
        ORDER BY coletado_em
    """).fetchall()
    conn.close()

    series = defaultdict(lambda: {"x": [], "y": []})
    for r in linhas:
        series[r["produto"]]["x"].append(r["coletado_em"])
        series[r["produto"]]["y"].append(r["preco"])

    plt.figure(figsize=(11, 6))
    for produto, dados in series.items():
        plt.plot(dados["x"], dados["y"], marker="o", label=produto)

    plt.title("Variação de preço ao longo do tempo")
    plt.xlabel("Coletado em")
    plt.ylabel("Preço (BRL)")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    CHARTS_DIR.mkdir(exist_ok=True)
    destino = CHARTS_DIR / "variacao_precos.png"
    plt.savefig(destino, dpi=120)
    print(f"\nGráfico salvo em: {destino}")


if __name__ == "__main__":
    relatorio_texto()
    grafico_variacao()
