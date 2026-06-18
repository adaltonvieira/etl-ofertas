import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))  # permite importar db

import pandas as pd
import streamlit as st
from db import get_connection


@st.cache_data(ttl=60)
def carregar_dados():
    conn = get_connection()
    linhas = conn.execute(
        "SELECT produto, preco, moeda, coletado_em FROM precos ORDER BY coletado_em"
    ).fetchall()
    conn.close()
    return pd.DataFrame(linhas)


st.set_page_config(page_title="Monitor de Precos", layout="wide")
st.title("Monitor de Precos")
st.caption("Dados coletados do PostgreSQL via pipeline ETL")

df = carregar_dados()

if df.empty:
    st.warning("Nenhum dado ainda. Rode 'python src/main.py' para coletar precos.")
    st.stop()

produtos = sorted(df["produto"].unique())
escolhido = st.selectbox("Escolha a moeda", produtos)

dados = df[df["produto"] == escolhido].sort_values("coletado_em")

preco_atual = dados["preco"].iloc[-1]
preco_anterior = dados["preco"].iloc[-2] if len(dados) > 1 else preco_atual
variacao = preco_atual - preco_anterior

col1, col2, col3 = st.columns(3)
col1.metric("Preco atual", f"R$ {preco_atual:.4f}", f"{variacao:+.4f}")
col2.metric("Minimo", f"R$ {dados['preco'].min():.4f}")
col3.metric("Maximo", f"R$ {dados['preco'].max():.4f}")

st.subheader(f"Variacao de {escolhido}")
serie = dados.set_index("coletado_em")["preco"]
st.line_chart(serie)

st.subheader("Historico")
st.dataframe(
    dados.sort_values("coletado_em", ascending=False),
    width="stretch",
)
