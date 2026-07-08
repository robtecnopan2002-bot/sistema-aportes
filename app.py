import streamlit as st
import time
import banco  # NOVO: Importa nosso arquivo de banco de dados permanente

# 1. INICIALIZAÇÃO DE VARIÁVEIS DO SISTEMA
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "tela_1"
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False  
if "plano_selecionado" not in st.session_state:
    st.session_state.plano_selecionado = None
if "valor_selecionado" not in st.session_state:
    st.session_state.valor_selecionado = 0.0

SENHA_MESTRE_ADMIN = "admin123"

PLANOS = {
    "Cobre": 300.00,
    "Bronze": 600.00,
    "Prata": 1000.00,
    "Ouro": 3000.00,
    "Diamante": 5000.00
}

def navegar_para(nova_tela):
    st.session_state.tela_atual = nova_tela
    st.rerun()

# --- TELA 1: VISUALIZAÇÃO DO PRODUTO ---
if st.session_state.tela_atual == "tela_1":
    st.title("🚀 Rendimento Financeiro Automatizado")
    st.subheader("Multiplique seu capital diariamente")
    st.markdown("---")
    st.metric(label="📊 Lucros Diários Estimados", value="0,1% a 1,0% ao dia")
    st.write("Nosso produto financeiro oferece rendimentos consistentes todos os dias diretamente na sua conta.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Estou de Acordo - Ir para Login / Cadastro", type="primary", use_container_width=True):
            navegar_para("tela_2")
    with col2:
        if st.button("⚙️ Acessar Painel Admin", type="secondary", use_container_width=True):
            navegar_para("tela_admin")
# --- TELA 2: LOGIN OU CADASTRO ---
elif st.session_state.tela_atual == "tela_2":
    st.title("🔐 Área de Acesso")
    aba_login, aba_cadastro = st.tabs(["Já tenho conta (Login)", "Quero me cadastrar"])
    
    with aba_login:
        login_cpf = st.text_input("Digite seu CPF (apenas números)", key="input_login_cpf")
        login_senha = st.text_input("Digite sua Senha", type="password", key="input_login_senha")
        if st.button("Entrar no Sistema", type="primary"):
            if login_cpf in st.session_state.usuarios_cadastrados:
                usuario = st.session_state.usuarios_cadastrados[login_cpf]
                if usuario["status"] == "Pendente":
                    st.warning("⚠️ Seu cadastro ainda precisa do aceite do Administrador (Tela 5).")
                elif usuario["senha"] == login_senha:
                    st.session_state.usuario_logado = login_cpf
                    st.success(f"Bem-vindo(a), {usuario['nome']}!")
                    time.sleep(1)
                    navegar_para("tela_3")
                else:
                    st.error("Senha incorreta.")
            else:
                st.error("CPF não encontrado.")
                
    with aba_cadastro:
        cad_nome = st.text_input("Nome Completo", key="reg_nome")
        cad_cpf = st.text_input("CPF (Apenas números)", key="reg_cpf")
        cad_tel = st.text_input("Telefone com DDD", key="reg_tel")
        cad_cep = st.text_input("CEP", key="reg_cep")
        cad_email = st.text_input("E-mail", key="reg_email")
        cad_senha = st.text_input("Crie uma Senha", type="password", key="reg_senha")
        if st.button("Finalizar Meu Cadastro", type="secondary"):
            if not (cad_nome and cad_cpf and cad_tel and cad_cep and cad_email and cad_senha):
                st.error("⚠️ Preencha todos os campos.")
            elif cad_cpf in st.session_state.usuarios_cadastrados:
                st.warning("⚠️ CPF já registrado.")
            else:
                st.session_state.usuarios_cadastrados[cad_cpf] = {
                    "nome": cad_nome, "cpf": cad_cpf, "telefone": cad_tel, "cep": cad_cep,
                    "email": cad_email, "senha": cad_senha, "status": "Pendente", "saldo": 0.0, "plano_ativo": "Nenhum"
                }
                st.success("✅ Cadastro realizado! Aguarde o aceite do administrador no painel.")
                
    st.markdown("---")
    if st.button("← Voltar para a Tela Inicial"):
        navegar_para("tela_1")

# --- TELA 3: PAINEL DO INVESTIDOR ---
elif st.session_state.tela_atual == "tela_3":
    cpf = st.session_state.usuario_logado
    user = st.session_state.usuarios_cadastrados[cpf]
    st.title("📥 Painel do Investidor")
    st.subheader(f"Seja bem-vindo, {user['nome']}.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="💰 Seu Saldo Disponível", value=f"R$ {user['saldo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col_s2:
        st.metric(label="📌 Plano Ativo", value=user['plano_ativo'])
        
    st.markdown("---")
    tab_fazer_aporte, tab_solicitar_saque = st.tabs(["Fazer Novo Aporte", "Solicitar Saque (Resgate)"])
    
    with tab_fazer_aporte:
        for nome_plano, valor_plano in PLANOS.items():
            col_info, col_botao = st.columns(2)  # CORRIGIDO: Passado o número 2 explicitamente
            with col_info:
                st.write(f"🔹 **Plano {nome_plano}** — Valor único:")
                st.subheader(f"R$ {valor_plano:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            with col_botao:
                st.write("") 
                if st.button(f"Escolher {nome_plano}", key=f"btn_{nome_plano}", type="primary"):
                    st.session_state.plano_selecionado = nome_plano
                    st.session_state.valor_selecionado = valor_plano
                    navegar_para("tela_4")
            st.markdown("---")
            
    with tab_solicitar_saque:
        if user["saldo"] <= 0:
            st.warning("Você não possui saldo disponível para realizar saques.")
        else:
            valor_saque = st.number_input("Valor do saque (R$)", min_value=1.0, max_value=user["saldo"], step=50.0)
            chave_pix_saque = st.text_input("Informe sua Chave PIX")
            if st.button("Confirmar Pedido de Saque", type="primary"):
                if chave_pix_saque:
                    st.session_state.historico_saques.append({
                        "id_saque": len(st.session_state.historico_saques) + 1, "cpf": cpf,
                        "nome": user["nome"], "valor": valor_saque, "chave_pix": chave_pix_saque, "status": "Pendente"
                    })
                    st.success("✅ Solicitação de saque enviada!")
                    time.sleep(1.5)
                    st.rerun()
        
    if st.button("← Sair / Fazer Logout"):
        st.session_state.usuario_logado = None
        navegar_para("tela_1")
# --- TELA 4: TELA DE PAGAMENTO VIA PIX ---
elif st.session_state.tela_atual == "tela_4":
    st.title("💸 Pagamento do Aporte")
    plano = st.session_state.plano_selecionado
    valor = st.session_state.valor_selecionado
    cpf_cliente = st.session_state.usuario_logado
    nome_cliente = st.session_state.usuarios_cadastrados[cpf_cliente]["nome"]
    
    st.subheader(f"Você escolheu o plano **{plano}**")
    st.info(f"Valor a pagar: **R$ {valor:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
    st.write("Escaneie o QR Code ou utilize a chave Copia e Cola:")
    st.image("https://qrserver.com", width=250)
    
    chave_copia_cola = f"00020101021126330014br.gov.bcb.pix0111123456789015204000053039865405{int(valor)}005802BR5913SISTEMA_APORT6009SAO_PAULO62070503***6304"
    st.text_area("Chave Pix Copia e Cola:", value=chave_copia_cola, height=90)
    st.markdown("---")
    
    if st.button("Confirmar que realizei o pagamento", type="primary", use_container_width=True):
        st.session_state.historico_aportes.append({
            "id_aporte": len(st.session_state.historico_aportes) + 1, "cpf": cpf_cliente,
            "nome": nome_cliente, "plano": plano, "valor": valor, "status": "Pendente"
        })
        st.success("✅ Notificação de pagamento enviada!")
        time.sleep(2)
        navegar_para("tela_3")
    if st.button("← Mudar de Plano"):
        navegar_para("tela_3")

# --- PAINEL DO ADMINISTRADOR (TELAS 5, 6 e 7) ---
elif st.session_state.tela_atual == "tela_admin":
    st.title("🛠️ Painel Administrativo Geral")
    
    # Se o administrador NÃO estiver logado, exibe a tela de login de segurança
    if not st.session_state.admin_logado:
        st.subheader("🔒 Acesso Restrito")
        senha_admin = st.text_input("Digite a senha master do sistema", type="password", key="input_senha_admin")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Verificar Senha", type="primary", use_container_width=True):
                if senha_admin == SENHA_MESTRE_ADMIN:
                    st.session_state.admin_logado = True
                    st.success("Acesso autorizado!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Senha incorreta! Acesso negado.")
        with col_b2:
            if st.button("← Voltar para a Home", type="secondary", use_container_width=True):
                navegar_para("tela_1")
                
    # Se o administrador JÁ estiver logado com sucesso, libera as Telas 5, 6 e 7
    else:
        col_logout_admin1, col_logout_admin2 = st.columns([3, 1])
        with col_logout_admin1:
            st.write("Gerencie os acessos, valide pagamentos e autorize os saques dos investidores.")
        with col_logout_admin2:
            if st.button("🔒 Sair do Painel Admin", type="secondary", use_container_width=True):
                st.session_state.admin_logado = False
                navegar_para("tela_1")
                
        st.markdown("---")
        
        aba_tela5, aba_tela6, aba_tela7 = st.tabs([
            "👥 Tela 5: Aceite de Cadastros", "💰 Tela 6: Autorizar Aportes", "💳 Tela 7: Autorizar Saques"
        ])
        
        with aba_tela5:
            st.subheader("Novos clientes aguardando autorização")
            clientes_pendentes = [u for u in st.session_state.usuarios_cadastrados.values() if u["status"] == "Pendente"]
            if not clientes_pendentes:
                st.info("Nenhum cadastro pendente.")
            else:
                for cl in clientes_pendentes:
                    with st.expander(f"📋 Cadastro de: {cl['nome']}"):
                        st.write(f"**CPF:** {cl['cpf']} | **Tel:** {cl['telefone']} | **CEP:** {cl['cep']}")
                        if st.button(f"Aprovar {cl['nome']}", key=f"aceite_{cl['cpf']}", type="primary"):
                            st.session_state.usuarios_cadastrados[cl['cpf']]["status"] = "Aprovado"
                            st.success("Cliente liberado!")
                            time.sleep(1)
                            st.rerun()

        with aba_tela6:
            st.subheader("Aportes solicitados por PIX")
            aportes_pendentes = [a for a in st.session_state.historico_aportes if a["status"] == "Pendente"]
            if not aportes_pendentes:
                st.info("Nenhum pagamento pendente.")
            else:
                for ap in aportes_pendentes:
                    with st.expander(f"💸 Aporte #{ap['id_aporte']} - {ap['nome']}"):
                        st.write(f"**Plano:** {ap['plano']} | **Valor:** R$ {ap['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                        if st.button(f"Confirmar PIX", key=f"conf_ap_{ap['id_aporte']}", type="primary"):
                            ap["status"] = "Aprovado"
                            st.session_state.usuarios_cadastrados[ap['cpf']]["saldo"] += ap['valor']
                            st.session_state.usuarios_cadastrados[ap['cpf']]["plano_ativo"] = ap['plano']
                            st.success("Saldo inserido!")
                            time.sleep(1)
                            st.rerun()

        with aba_tela7:
            st.subheader("Pedidos de Resgate de Lucros")
            saques_pendentes = [s for s in st.session_state.historico_saques if s["status"] == "Pendente"]
            if not saques_pendentes:
                st.info("Não existem saques aguardando autorização.")
            else:
                for sq in saques_pendentes:
                    with st.expander(f"💳 Saque #{sq['id_saque']} - {sq['nome']}"):
                        st.write(f"**Valor:** R$ {sq['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                        st.write(f"**Chave PIX:** {sq['chave_pix']}")
                        if st.button(f"Liquidar Saque", key=f"conf_sq_{sq['id_saque']}", type="primary"):
                            sq["status"] = "Concluído"
                            st.session_state.usuarios_cadastrados[sq['cpf']]["saldo"] -= sq['valor']
                            st.success("Saque autorizado e debitado!")
                            time.sleep(1)
                            st.rerun()
