import streamlit as st

# Inicialização da navegação se não existir
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "tela_1"

# TELA 1: Visualização do Produto
if st.session_state.tela_atual == "tela_1":
    st.title("🚀 Rendimento Financeiro Automatizado")
    st.subheader("Multiplique seu capital diariamente")
    
    st.markdown("---")
    
    # Exibição do ganho
    st.metric(label="📊 Lucros Diários Estimados", value="0,1% a 1,0% ao dia")
    
    st.write(
        "Nosso produto financeiro oferece rendimentos consistentes todos os dias "
        "diretamente na sua conta de forma automatizada e transparente."
    )
    
    st.markdown("---")
    
    # Botão de ação
    if st.button("Estou de Acordo - Ir para Login / Cadastro", type="primary", use_container_width=True):
        st.success("Perfeito! No próximo passo faremos a tela de acesso.")
