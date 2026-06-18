from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
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
    print("\n=== Relatorio de precos ===")
    for r in linhas:
        print(f"{r['produto']}: {r['coletas']} coletas | "
              f"min {r['minimo']} | max {r['maximo']} | media {r['media']}")


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

    produtos = list(series.keys())
    n = len(produtos)

    # Um painel por produto, cada um com seu proprio eixo Y.
    fig, axes = plt.subplots(n, 1, figsize=(11, 3 * n), sharex=True)
    if n == 1:
        axes = [axes]

    cores = plt.cm.tab10.colors
    for ax, produto, cor in zip(axes, produtos, cores):
        dados = series[produto]
        ax.plot(dados["x"], dados["y"], marker="o", color=cor)
        ax.set_title(produto)
        ax.set_ylabel("Preco (BRL)")
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Coletado em")
    plt.setp(axes[-1].get_xticklabels(), rotation=45, ha="right")
    fig.suptitle("Variacao de preco ao longo do tempo")
    fig.tight_layout()

    CHARTS_DIR.mkdir(exist_ok=True)
    destino = CHARTS_DIR / "variacao_precos.png"
    fig.savefig(destino, dpi=120)
    print(f"\nGrafico salvo em: {destino}")


if __name__ == "__main__":
    relatorio_texto()
    grafico_variacao()
