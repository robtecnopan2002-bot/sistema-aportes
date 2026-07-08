pythonimport streamlit as st
import time

# 1. INICIALIZAÇÃO DE VARIÁVEIS DO SISTEMA
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "tela_1"
if "usuarios_cadastrados" not in st.session_state:
    st.session_state.usuarios_cadastrados = {}  # Guarda os cadastros usando o CPF como chave
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# Função auxiliar para trocar de tela
def navegar_para(nova_tela):
    st.session_state.tela_atual = nova_tela
    st.rerun()


# ==========================================
# TELA 1: VISUALIZAÇÃO DO PRODUTO
# ==========================================
if st.session_state.tela_atual == "tela_1":
    st.title("🚀 Rendimento Financeiro Automatizado")
    st.subheader("Multiplique seu capital diariamente")
    
    st.markdown("---")
    st.metric(label="📊 Lucros Diários Estimados", value="0,1% a 1,0% ao dia")
    
    st.write(
        "Nosso produto financeiro oferece rendimentos consistentes todos os dias "
        "diretamente na sua conta de forma automatizada e transparente."
    )
    st.markdown("---")
    
    if st.button("Estou de Acordo - Ir para Login / Cadastro", type="primary", use_container_width=True):
        navegar_para("tela_2")


# ==========================================
# TELA 2: LOGIN OU CADASTRO
# ==========================================
elif st.session_state.tela_atual == "tela_2":
    st.title("🔐 Área de Acesso")
    
    # Criando abas para separar o Login do Cadastro
    aba_login, aba_cadastro = st.tabs(["Já tenho conta (Login)", "Quero me cadastrar"])
    
    # --- FLUXO DE LOGIN ---
    with aba_login:
        st.subheader("Identifique-se para acessar")
        login_cpf = st.text_input("Digite seu CPF (apenas números)", key="input_login_cpf")
        login_senha = st.text_input("Digite sua Senha", type="password", key="input_login_senha")
        
        if st.button("Entrar no Sistema", type="primary"):
            if login_cpf in st.session_state.usuarios_cadastrados:
                usuario = st.session_state.usuarios_cadastrados[login_cpf]
                if usuario["senha"] == login_senha:
                    st.session_state.usuario_logado = login_cpf
                    st.success(f"Bem-vindo(a), {usuario['nome']}!")
                    time.sleep(1)
                    # Por enquanto, mostramos apenas uma mensagem de sucesso
                    st.info("Sucesso! No próximo passo faremos a Tela 3 (Aportes).")
                else:
                    st.error("Senha incorreta. Tente novamente.")
            else:
                st.error("CPF não encontrado. Vá na aba de cadastro ao lado.")
                
    # --- FLUXO DE CADASTRO ---
    with aba_cadastro:
        st.subheader("Preencha seus dados para começar")
        
        cad_nome = st.text_input("Nome Completo", key="reg_nome")
        cad_cpf = st.text_input("CPF (Apenas números)", key="reg_cpf")
        cad_tel = st.text_input("Telefone com DDD", key="reg_tel")
        cad_cep = st.text_input("CEP", key="reg_cep")
        cad_email = st.text_input("E-mail", key="reg_email")
        cad_senha = st.text_input("Crie uma Senha", type="password", key="reg_senha")
        
        if st.button("Finalizar Meu Cadastro", type="secondary"):
            # Validação simples se todos os campos foram preenchidos
            if not (cad_nome and cad_cpf and cad_tel and cad_cep and cad_email and cad_senha):
                st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
            elif cad_cpf in st.session_state.usuarios_cadastrados:
                st.warning("⚠️ Este CPF já está registrado em nossa base.")
            else:
                # Salva o novo usuário no dicionário em memória
                st.session_state.usuarios_cadastrados[cad_cpf] = {
                    "nome": cad_nome,
                    "cpf": cad_cpf,
                    "telefone": cad_tel,
                    "cep": cad_cep,
                    "email": cad_email,
                    "senha": cad_senha,
                    "status": "Pendente" # Será usado na tela do administrador depois
                }
                st.success("✅ Cadastro realizado com sucesso! Agora você já pode fazer login na aba ao lado.")
                
    # Botão de segurança para voltar
    st.markdown("---")
    if st.button("← Voltar para a Tela Inicial"):
        navegar_para("tela_1")
