from db import init_db
from extract import extrair_precos
from load import carregar_precos


def coletar():
    init_db()                  # garante que a tabela existe
    itens = extrair_precos()   # E + T
    carregar_precos(itens)     # L


if __name__ == "__main__":
    coletar()
