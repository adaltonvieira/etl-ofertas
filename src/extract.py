import requests

API_URL = "https://economia.awesomeapi.com.br/last/"

PRODUTOS = ["USD-BRL", "EUR-BRL", "BTC-BRL"]


def extrair_precos(pares=PRODUTOS):
    """Busca as cotações atuais e devolve uma lista limpa de dicionários."""
    url = API_URL + ",".join(pares)
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()

    resultados = []
    for _, info in dados.items():
        resultados.append({
            "produto": info["name"],
            "preco": float(info["bid"]),
            "moeda": info["codein"],
        })
    return resultados


if __name__ == "__main__":
    for item in extrair_precos():
        print(item)
