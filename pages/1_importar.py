import streamlit as st
import pandas as pd

st.title("📂 Importar lançamentos")

# =========================
# BOTÃO VER EXEMPLO
# =========================
if st.button("✨ Ver exemplo"):
    data = {
        "data": [
            "2026-01-05","2026-01-10","2026-01-15","2026-01-20","2026-01-25",
            "2026-02-02","2026-02-08","2026-02-14","2026-02-18","2026-02-25",
            "2026-03-03","2026-03-07","2026-03-12","2026-03-18","2026-03-25",
            "2026-04-01","2026-04-06","2026-04-10","2026-04-15","2026-04-22",
            "2026-05-03","2026-05-08","2026-05-12","2026-05-18","2026-05-25",
            "2026-06-02","2026-06-07","2026-06-12","2026-06-18","2026-06-25"
        ],
        "categoria": [
            "Salário","Alimentação","Transporte","Lazer","Moradia",
            "Salário","Alimentação","Transporte","Saúde","Lazer",
            "Salário","Alimentação","Transporte","Educação","Lazer",
            "Salário","Alimentação","Transporte","Saúde","Moradia",
            "Salário","Alimentação","Transporte","Lazer","Educação",
            "Salário","Alimentação","Transporte","Saúde","Moradia"
        ],
        "valor": [
            3500,-120,-80,-200,-900,
            3500,-150,-90,-300,-180,
            3500,-130,-85,-400,-220,
            3500,-160,-95,-250,-900,
            3500,-140,-88,-210,-350,
            3500,-170,-92,-270,-900
        ],
        "canal": [
            "Pix","Cartão","Pix","Cartão","Boleto",
            "Pix","Cartão","Pix","Cartão","Boleto",
            "Pix","Cartão","Pix","Cartão","Boleto",
            "Pix","Cartão","Pix","Cartão","Boleto",
            "Pix","Cartão","Pix","Cartão","Boleto",
            "Pix","Cartão","Pix","Cartão","Boleto"
        ]
        "tipo":  [
            "Receita","Despesa","Despesa","Despesa","Despesa",
            "Receita","Despesa","Despesa","Despesa","Despesa",
            "Receita","Despesa","Despesa","Despesa","Despesa",
            "Receita","Despesa","Despesa","Despesa","Despesa",
            "Receita","Despesa","Despesa","Despesa","Despesa",
            "Receita","Despesa","Despesa","Despesa","Despesa"
    ],
    }

    df = pd.DataFrame(data)

    # tratamento
    df["data"] = pd.to_datetime(df["data"])
    df = df.dropna(subset=["data", "valor"])

    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["mes_nome"] = df["data"].dt.strftime("%B")

    st.session_state["df"] = df
    st.success("Exemplo carregado com sucesso!")


# =========================
# UPLOAD DE ARQUIVO
# =========================
uploaded_file = st.file_uploader(
    "Envie seu arquivo (CSV ou Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        nome = uploaded_file.name.lower()

        if nome.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif nome.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Formato não suportado.")
            st.stop()

        # validação
        colunas = ["data", "categoria", "valor"]
        if not all(c in df.columns for c in colunas):
            st.error("O arquivo precisa conter: data, categoria, valor")
            st.stop()

        # tratamento
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data", "valor"])

        df["ano"] = df["data"].dt.year
        df["mes"] = df["data"].dt.month
        df["mes_nome"] = df["data"].dt.strftime("%B")

        # se não tiver canal, cria (evita erro no dashboard)
        if "canal" not in df.columns:
            df["canal"] = "Não informado"

        st.session_state["df"] = df

        st.success("Arquivo importado com sucesso!")

    except Exception as e:
        st.error(f"Erro ao importar: {e}")


# =========================
# PREVIEW
# =========================
if "df" in st.session_state:
    st.subheader("Pré-visualização")
    st.dataframe(st.session_state["df"], use_container_width=True)


# =========================
# BOTÃO LIMPAR
# =========================
if st.button("🗑️ Limpar dados"):
    if "df" in st.session_state:
        del st.session_state["df"]
    st.rerun()