# ETL de Ofertas — Monitor de Preços

Pipeline ETL didático em Python que coleta preços de uma API pública, armazena o histórico em PostgreSQL, expõe os dados por uma API REST (FastAPI) e gera relatório e gráfico de variação.

Projeto construído de forma incremental: comecou em SQLite, foi migrado para PostgreSQL e ganhou uma API web.

## O que faz

- Extract: busca cotações em tempo real na AwesomeAPI (dólar, euro e bitcoin em reais).
- Transform: limpa o JSON da API, mantendo apenas produto, preço e moeda.
- Load: grava cada coleta no PostgreSQL com carimbo de data/hora.
- Relatório: consultas SQL (mín./máx./média e variação com window function) e gráfico com matplotlib.
- API: expõe os dados por HTTP com documentação interativa automática.

## Estrutura

    etl-ofertas/
    ├── charts/              # graficos gerados
    ├── src/
    │   ├── db.py            # conexao (psycopg) + criacao da tabela e indice
    │   ├── extract.py       # etapa E/T: busca e limpa os dados da API
    │   ├── load.py          # etapa L: grava no PostgreSQL
    │   ├── main.py          # orquestra a coleta (E + T + L)
    │   ├── report.py        # relatorio + grafico
    │   ├── sql.py           # utilitario para rodar consultas SQL ad-hoc
    │   └── api.py           # API REST (FastAPI)
    └── requirements.txt

## Pré-requisitos

PostgreSQL instalado e rodando. Crie o banco e o usuário:

    sudo -u postgres psql
    CREATE USER adalton WITH PASSWORD 'sua_senha';
    CREATE DATABASE etl_ofertas OWNER adalton;
    \q

## Como rodar

    git clone https://github.com/adaltonvieira/etl-ofertas.git
    cd etl-ofertas
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Crie um arquivo `.env` na raiz com suas credenciais:

    DB_HOST=localhost
    DB_NAME=etl_ofertas
    DB_USER=adalton
    DB_PASSWORD=sua_senha

Colete os dados e gere o relatorio:

    python src/main.py     # coleta precos (rode varias vezes para acumular historico)
    python src/report.py   # gera relatorio e grafico

## API REST

Suba o servidor:

    uvicorn api:app --reload --app-dir src

Endpoints:

- `GET /` — informacoes da API
- `GET /precos` — coletas recentes (parametros: `produto`, `limite`)
- `GET /precos/variacao` — variacao entre coletas (window function)
- `GET /docs` — documentacao interativa (Swagger UI)

Exemplo: http://localhost:8000/precos?produto=Dolar&limite=5

## Exemplo de saida

![Variacao de precos](charts/variacao_precos.png)

## Tecnologias

Python, PostgreSQL, psycopg, FastAPI, uvicorn, python-dotenv, matplotlib

## Proximos passos

- Busca semantica de produtos com embeddings (pgvector / Chroma).
