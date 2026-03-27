import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Financial Insight Dashboard")

ARQUIVO = "data/dados.csv"

# =========================
# FUNÇÕES
# =========================
def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def perc(v):
    return f"{v:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

def carregar():
    if os.path.exists(ARQUIVO):
        return pd.read_csv(ARQUIVO)
    return pd.DataFrame(columns=["data","tipo","categoria","canal","descricao","valor"])

def salvar(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(ARQUIVO, index=False)

# =========================
# CARREGAR DADOS
# =========================
if "df" not in st.session_state:
    st.session_state["df"] = carregar()

df = st.session_state["df"]

# =========================
# 📥 MODELO CSV (SEM ERRO)
# =========================
st.subheader("📥 Modelo para Importação")

modelo = pd.DataFrame([
    {
        "data": "2025-01-10",
        "tipo": "Receita",
        "categoria": "Vendas de Produtos",
        "canal": "Site",
        "descricao": "Venda exemplo",
        "valor": 2500
    },
    {
        "data": "2025-01-15",
        "tipo": "Despesa",
        "categoria": "Marketing",
        "canal": "Marketing",
        "descricao": "Campanha exemplo",
        "valor": 800
    }
])

csv = modelo.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Baixar modelo CSV",
    data=csv,
    file_name="modelo_importacao.csv",
    mime="text/csv"
)

# =========================
# FORMULÁRIO
# =========================
st.subheader("➕ Adicionar lançamento")

tipo = st.selectbox("Tipo", ["Receita", "Despesa"])

if tipo == "Receita":
    categorias = ["Vendas de Produtos","Vendas de Serviços","Recebimentos","Consultoria","Outros"]
    canais = ["Site","Loja Física","Marketplace","Redes Sociais","WhatsApp","Indicação"]
else:
    categorias = ["Marketing","Salários","Impostos","Serviços","Aluguel","Fornecedores","Outros"]
    canais = ["Financeiro","Administrativo","Compras","Marketing","Vendas"]

categoria = st.selectbox("Categoria", categorias)
canal = st.selectbox("Canal", canais)
descricao = st.text_input("Descrição")

data = st.date_input("Data", format="DD/MM/YYYY")
valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

if st.button("Adicionar"):
    novo = pd.DataFrame([{
        "data": data,
        "tipo": tipo,
        "categoria": categoria,
        "canal": canal,
        "descricao": descricao,
        "valor": valor
    }])

    st.session_state["df"] = pd.concat([df, novo], ignore_index=True)
    salvar(st.session_state["df"])
    st.success("Salvo com sucesso!")

# =========================
# DASHBOARD
# =========================
df = st.session_state["df"]

if df.empty:
    st.warning("Sem dados")
else:
    df["data"] = pd.to_datetime(df["data"])
    df["valor"] = pd.to_numeric(df["valor"])

    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month

    # =========================
    # FILTROS
    # =========================
    st.sidebar.header("Filtros")

    anos = sorted(df["ano"].unique())
    ano = st.sidebar.selectbox("Ano", anos)

    meses_map = {
        1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
        7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"
    }

    meses_lista = ["Todos"] + sorted(df["mes"].unique())

    mes = st.sidebar.selectbox(
        "Mês",
        meses_lista,
        index=0,
        format_func=lambda x: "Todos" if x == "Todos" else meses_map[x]
    )

    if mes == "Todos":
        df_f = df[df["ano"] == ano]
    else:
        df_f = df[(df["ano"] == ano) & (df["mes"] == mes)]

    # =========================
    # MÉTRICAS
    # =========================
    receitas = df_f[df_f["tipo"] == "Receita"]["valor"].sum()
    despesas = df_f[df_f["tipo"] == "Despesa"]["valor"].sum()
    resultado = receitas - despesas
    margem = (resultado / receitas * 100) if receitas > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Receitas", moeda(receitas))
    col2.metric("Despesas", moeda(despesas))
    col3.metric("Resultado", moeda(resultado))
    col4.metric("Margem", perc(margem))

    # =========================
    # TABELA COM EXCLUSÃO
    # =========================
    st.subheader("📋 Gerenciar Lançamentos")

    df_exibir = df_f.copy()
    df_exibir["data"] = df_exibir["data"].dt.strftime("%d/%m/%Y")
    df_exibir["valor"] = df_exibir["valor"].apply(moeda)

    df_exibir.insert(0, "Selecionar", False)

    edited_df = st.data_editor(
        df_exibir,
        use_container_width=True,
        num_rows="dynamic"
    )

    col1, col2 = st.columns(2)

    # excluir selecionados
    with col1:
        if st.button("🗑️ Excluir selecionados"):
            selecionados = edited_df[edited_df["Selecionar"] == True]

            if not selecionados.empty:
                df_original = st.session_state["df"]
                df_novo = df_original.drop(selecionados.index)

                st.session_state["df"] = df_novo
                salvar(df_novo)

                st.success("Registros excluídos")
                st.rerun()

    # excluir todos
    with col2:
        if st.button("⚠️ Excluir TODOS"):
            st.session_state["df"] = pd.DataFrame(columns=df.columns)
            salvar(st.session_state["df"])

            st.warning("Todos os dados foram apagados")
            st.rerun()