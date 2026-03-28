# 📊 FID - Financial Intelligence Dashboard

Dashboard interativo desenvolvido com Streamlit para visualização e análise de dados financeiros.

## 🎯 Objetivo

O FID (Financial Intelligence Dashboard) permite a exploração visual de receitas e despesas, facilitando a compreensão dos dados financeiros por meio de gráficos e filtros por período (ano e mês).

## 🚀 Funcionalidades

* 📥 Importação de dados via arquivo CSV
* 📊 Visualização de receitas e despesas
* 📅 Filtros por ano e mês
* 📈 Geração de gráficos para análise
* 🔎 Navegação entre páginas (importação e análises)

## 🛠️ Tecnologias utilizadas

* Python
* Streamlit
* Pandas
* Plotly / Matplotlib

## ▶️ Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/Mafaleiros17/fid-financial-dashboard.git
```

2. Acesse a pasta do projeto:

```bash
cd fid-financial-dashboard
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
streamlit run dashboard.py
```

## 📁 Estrutura do projeto

* `dashboard.py` → arquivo principal da aplicação
* `pages/`

  * `1_importar.py` → página de importação de dados
  * `2_analises.py` → página de análises e gráficos
* `data/`

  * `dados.csv` → base de dados para testes
  * `data.json` → dados auxiliares (se aplicável)
* `utils.py` → funções auxiliares do projeto
* `requirements.txt` → dependências do projeto

## 👤 Autora

Projeto desenvolvido por Margareth Faleiros.

---

💡 Projeto desenvolvido como parte do portfólio em Data Analytics.
