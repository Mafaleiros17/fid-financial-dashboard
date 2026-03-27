import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análises", layout="wide")

st.title("📊 Análises")

# =========================
# VALIDAÇÃO
# =========================
if "df" not in st.session_state or st.session_state["df"].empty:
    st.warning("Adicione ou importe dados primeiro.")
    st.stop()

df = st.session_state["df"].copy()

# =========================
# FUNÇÕES
# =========================
def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def perc(v):
    return f"{v:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular(df):
    r = df[df["tipo"] == "Receita"]["valor"].sum()
    d = df[df["tipo"] == "Despesa"]["valor"].sum()
    res = r - d
    m = (res / r * 100) if r > 0 else 0
    return r, d, res, m

# =========================
# TRATAMENTO
# =========================
df["data"] = pd.to_datetime(df["data"])
df["valor"] = pd.to_numeric(df["valor"])

df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month

meses_map = {
    1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
    7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"
}

df["ano_str"] = df["ano"].astype(str)

# =========================
# FILTROS
# =========================
st.sidebar.header("Filtros")

anos = sorted(df["ano"].unique())
meses_lista = ["Todos"] + list(range(1,13))

anos_sel = st.sidebar.multiselect("Anos", anos, default=anos)
meses_sel = st.sidebar.multiselect("Meses", meses_lista, default=["Todos"])

canais = sorted(df["canal"].dropna().unique())
categorias = sorted(df["categoria"].dropna().unique())

canais_sel = st.sidebar.multiselect("Canal", canais, default=canais)
categorias_sel = st.sidebar.multiselect("Categoria", categorias, default=categorias)

# =========================
# APLICAR FILTROS
# =========================
df_filtrado = df[df["ano"].isin(anos_sel)]

if "Todos" not in meses_sel:
    df_filtrado = df_filtrado[df_filtrado["mes"].isin(meses_sel)]

df_filtrado = df_filtrado[df_filtrado["canal"].isin(canais_sel)]
df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categorias_sel)]

# =========================
# MÉTRICAS
# =========================
r,d,res,m = calcular(df_filtrado)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Receitas", moeda(r))
col2.metric("Despesas", moeda(d))
col3.metric("Resultado", moeda(res))
col4.metric("Margem", perc(m))

# =========================
# RECEITAS
# =========================
st.subheader("💰 Receitas por Canal")

rec = df_filtrado[df_filtrado["tipo"]=="Receita"] \
    .groupby(["canal","ano_str"])["valor"].sum().reset_index()

fig1 = px.bar(rec, x="canal", y="valor", color="ano_str", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# =========================
# DESPESAS
# =========================
st.subheader("💸 Despesas por Categoria")

desp = df_filtrado[df_filtrado["tipo"]=="Despesa"] \
    .groupby(["categoria","ano_str"])["valor"].sum().reset_index()

fig2 = px.bar(desp, x="categoria", y="valor", color="ano_str", barmode="group")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# RESULTADO
# =========================
st.subheader("📈 Resultado Mensal")

resumo = df_filtrado.groupby(["ano","mes","tipo"])["valor"].sum().reset_index()

pivot = resumo.pivot_table(
    index=["ano","mes"],
    columns="tipo",
    values="valor",
    fill_value=0
).reset_index()

pivot["resultado"] = pivot["Receita"] - pivot["Despesa"]
pivot = pivot.sort_values("mes")
pivot["mes_nome"] = pivot["mes"].map(meses_map)

fig3 = px.line(
    pivot,
    x="mes_nome",
    y="resultado",
    color=pivot["ano"].astype(str),
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# TOP 5 (AGORA NO LUGAR CERTO)
# =========================
st.subheader("🏆 Destaques")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 5 Receitas (Canal)**")
    top_rec = (
        df_filtrado[df_filtrado["tipo"]=="Receita"]
        .groupby("canal")["valor"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.dataframe(top_rec.apply(moeda))

with col2:
    st.markdown("**Top 5 Despesas (Categoria)**")
    top_desp = (
        df_filtrado[df_filtrado["tipo"]=="Despesa"]
        .groupby("categoria")["valor"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.dataframe(top_desp.apply(moeda))

# =========================
# TABELA
# =========================
st.subheader("📋 Dados")

df_exibir = df_filtrado.copy()
df_exibir["data"] = df_exibir["data"].dt.strftime("%d/%m/%Y")
df_exibir["valor"] = df_exibir["valor"].apply(moeda)

st.dataframe(df_exibir, use_container_width=True)