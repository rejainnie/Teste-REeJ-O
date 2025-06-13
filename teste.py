import streamlit as st
import pandas as pd

import seaborn as sns

# Configuração da página para uma estética agradável
st.set_page_config(layout="centered", page_title="Formulário de Registro de Dados", page_icon="📝")

# Título principal com estilo UX/Design
st.markdown(
    """
    <style>
    .main-title {
        font-size: 3em;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
        box-shadow: inset 1px 1px 3px rgba(0,0,0,0.1);
    }
    .dataframe {
        font-size: 0.9em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="main-title">📝 Registro de Dados Demográficos</p>', unsafe_allow_html=True)
st.write("Preencha os campos abaixo para registrar informações de sexo e idade. Os dados serão exibidos e analisados em gráficos.")

# Inicializa o dataframe no Session State se ele ainda não existir
if 'df_registros' not in st.session_state:
    st.session_state.df_registros = pd.DataFrame(columns=['Sexo', 'Idade'])

# Formulário para entrada de dados
with st.form("form_registro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        sexo_input = st.selectbox("Sexo:", ["Masculino", "Feminino", "Outro"], help="Selecione o sexo da pessoa.")
    with col2:
        idade_input = st.number_input("Idade:", min_value=0, max_value=120, value=25, step=1, help="Digite a idade da pessoa.")

    # Botão de registro centralizado e com margem
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    submit_button = st.form_submit_button("Registrar Dados")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit_button:
        # Adiciona o novo registro ao DataFrame
        novo_registro = pd.DataFrame([{'Sexo': sexo_input, 'Idade': idade_input}])
        st.session_state.df_registros = pd.concat([st.session_state.df_registros, novo_registro], ignore_index=True)
        st.success("Dados registrados com sucesso!")

# Exibição da tabela de registros
st.markdown("---") # Divisor visual para melhor UX
st.subheader("📋 Dados Registrados")

if not st.session_state.df_registros.empty:
    st.dataframe(st.session_state.df_registros)
else:
    st.info("Nenhum dado registrado ainda. Por favor, preencha o formulário acima.")

# Se houver dados, exibir os gráficos
if not st.session_state.df_registros.empty:
    st.markdown("---") # Divisor visual
    st.subheader("📊 Estatísticas dos Registros")

    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        st.markdown("### Distribuição por Sexo")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sex_counts = st.session_state.df_registros['Sexo'].value_counts()
        sns.barplot(x=sex_counts.index, y=sex_counts.values, ax=ax1, palette='viridis')
        ax1.set_xlabel("Sexo")
        ax1.set_ylabel("Número de Registros")
        ax1.set_title("Contagem de Registros por Sexo")
        ax1.tick_params(axis='x', rotation=45) # Rotaciona os labels para melhor visualização
        plt.tight_layout() # Ajusta o layout para evitar sobreposição
        st.pyplot(fig1)

    with col_graph2:
        st.markdown("### Distribuição de Idades")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.histplot(st.session_state.df_registros['Idade'], bins=5, kde=True, ax=ax2, color='skyblue')
        ax2.set_xlabel("Idade")
        ax2.set_ylabel("Frequência")
        ax2.set_title("Distribuição de Idades dos Registrados")
        plt.tight_layout()
        st.pyplot(fig2)

else:
    st.warning("Para visualizar os gráficos, por favor, registre alguns dados primeiro.")

st.markdown("---")
st.info("Desenvolvido com carinho para você, combinando funcionalidade e uma ótima experiência de usuário.")
