# ETL de Ofertas — Monitor de Preços

Pipeline ETL didático em Python que coleta preços de uma API pública, armazena o histórico em SQLite e gera relatório e gráfico de variação ao longo do tempo.

## O que faz

- Extract: busca cotações em tempo real na AwesomeAPI (dólar, euro e bitcoin em reais).
- Transform: limpa o JSON da API, mantendo apenas produto, preço e moeda.
- Load: grava cada coleta no SQLite com carimbo de data/hora.
- Relatório: consultas SQL (mín./máx./média e variação) e gráfico de linha com matplotlib.

A fonte de dados é facilmente substituível: trocando apenas a etapa de extração, o mesmo pipeline serve para preços de produtos via API ou scraping.

## Estrutura

    etl-ofertas/
    ├── data/                # banco SQLite (gerado localmente)
    ├── charts/              # graficos gerados
    ├── src/
    │   ├── db.py            # conexao + criacao da tabela e indice
    │   ├── extract.py       # etapa E/T: busca e limpa os dados da API
    │   ├── load.py          # etapa L: grava no SQLite
    │   ├── main.py          # orquestra a coleta (E + T + L)
    │   ├── report.py        # relatorio + grafico
    │   └── sql.py           # utilitario para rodar consultas SQL ad-hoc
    └── requirements.txt

## Como rodar

    git clone https://github.com/adaltonvieira/etl-ofertas.git
    cd etl-ofertas
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python src/main.py
    python src/report.py

## Exemplo de saida

![Variacao de precos](charts/variacao_precos.png)

## Exemplo de consulta SQL

Variacao de preco entre uma coleta e a anterior (window function):

    python src/sql.py "SELECT produto, coletado_em, preco, ROUND(preco - LAG(preco) OVER (PARTITION BY produto ORDER BY coletado_em), 4) AS variacao FROM precos ORDER BY produto, coletado_em"

## Tecnologias

Python, SQLite, requests, matplotlib

## Proximos passos

- Migracao para PostgreSQL com API REST (FastAPI) e migrations (Alembic).
- Busca semantica de produtos com embeddings (pgvector / Chroma).
