import streamlit as st
import pandas as pd

st.title("📂 Importar lançamentos")

if st.button("✨ Ver exemplo"):
    import pandas as pd
    st.session_state["df"] = pd.read_csv("data/dados.csv")

uploaded_file = st.file_uploader(
    "Envie seu arquivo (CSV ou Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        nome = uploaded_file.name.lower()

        # leitura do arquivo
        if nome.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif nome.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Formato não suportado.")
            st.stop()

        # validação de colunas
        colunas = ["data", "categoria", "valor"]
        if not all(c in df.columns for c in colunas):
            st.error("O arquivo precisa conter: data, categoria, valor")
            st.stop()

        # tratamento de dados
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data", "valor"])

        # criação de colunas auxiliares
        df["ano"] = df["data"].dt.year
        df["mes"] = df["data"].dt.month
        df["mes_nome"] = df["data"].dt.strftime("%B")

        # salvar na sessão
        st.session_state["df"] = df

        st.success("Arquivo importado com sucesso!")

        # preview
        st.subheader("Pré-visualização")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao importar: {e}")

# botão limpar
if st.button("🗑️ Limpar dados"):
    if "df" in st.session_state:
        del st.session_state["df"]
    st.rerun()