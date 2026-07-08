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


# ==========================================
# TELA 3: INFORMA OS APORTES
# ==========================================
elif st.session_state.tela_atual == "tela_3":
    cpf = st.session_state.usuario_logado
    nome_usuario = st.session_state.usuarios_cadastrados[cpf]["nome"] if cpf else "Usuário"
    
    st.title("📥 Escolha seu Plano de Aporte")
    st.subheader(f"Seja bem-vindo, {nome_usuario}. Selecione abaixo o valor que deseja aportar:")
    
    st.markdown("---")
    
    # Cria colunas visuais para exibir os planos organizados
    for nome_plano, valor_plano in PLANOS.items():
        col_info, col_botao = st.columns([3, 1])
        with col_info:
            st.write(f"🔹 **Plano {nome_plano}** — Valor único de Investimento:")
            st.subheader(f"R$ {valor_plano:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        with col_botao:
            st.write("") # Apenas espaçamento
            if st.button(f"Escolher {nome_plano}", key=f"btn_{nome_plano}", type="primary"):
                st.session_state.plano_selecionado = nome_plano
                st.session_state.valor_selecionado = valor_plano
                navegar_para("tela_4")
        st.markdown("---")
        
    if st.button("← Sair / Voltar"):
        st.session_state.usuario_logado = None
        navegar_para("tela_1")


# ==========================================
# TELA 4: TELA DE PAGAMENTO VIA PIX
# ==========================================
elif st.session_state.tela_atual == "tela_4":
    st.title("💸 Pagamento do Aporte")
    
    plano = st.session_state.plano_selecionado
    valor = st.session_state.valor_selecionado
    
    st.subheader(f"Você escolheu o plano **{plano}**")
    st.info(f"Valor a pagar: **R$ {valor:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.write("Escaneie o QR Code abaixo pelo aplicativo do seu banco ou utilize a chave Copia e Cola:")
    
    # Gera uma imagem demonstrativa de QR Code
    st.image("https://qrserver.com", width=250)
    
    # Texto simulação de cópia e cola
    chave_copia_cola = f"00020101021126330014br.gov.bcb.pix0111123456789015204000053039865405{int(valor)}005802BR5913SISTEMA_APORT6009SAO_PAULO62070503***6304"
    st.text_area("Chave Pix Copia e Cola:", value=chave_copia_cola, height=90)
    
    st.markdown("---")
    
    if st.button("Confirmar que realizei o pagamento", type="primary", use_container_width=True):
        st.success("✅ Pagamento enviado para validação! No próximo passo faremos as telas do Administrador para aprovar este pedido.")
        time.sleep(3)
        navegar_para("tela_3")
        
    if st.button("← Mudar de Plano"):
        navegar_para("tela_3")
