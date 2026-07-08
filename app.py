import streamlit as st
import time

# 1. INICIALIZAÇÃO DE VARIÁVEIS DO SISTEMA
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "tela_1"
if "usuarios_cadastrados" not in st.session_state:
    st.session_state.usuarios_cadastrados = {}  # Guarda os cadastros usando o CPF como chave
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "plano_selecionado" not in st.session_state:
    st.session_state.plano_selecionado = None
if "valor_selecionado" not in st.session_state:
    st.session_state.valor_selecionado = 0.0

# Novas variáveis para controle do Administrador (Telas 5, 6 e 7)
if "historico_aportes" not in st.session_state:
    st.session_state.historico_aportes = []  # Lista de dicionários de aportes
if "historico_saques" not in st.session_state:
    st.session_state.historico_saques = []    # Lista de dicionários de saques

# Dicionário com os valores dos planos da Tela 3
PLANOS = {
    "Cobre": 300.00,
    "Bronze": 600.00,
    "Prata": 1000.00,
    "Ouro": 3000.00,
    "Diamante": 5000.00
}

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
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Estou de Acordo - Ir para Login / Cadastro", type="primary", use_container_width=True):
            navegar_para("tela_2")
    with col2:
        if st.button("⚙️ Acessar Painel Admin", type="secondary", use_container_width=True):
            navegar_para("tela_admin")


# ==========================================
# TELA 2: LOGIN OU CADASTRO
# ==========================================
elif st.session_state.tela_atual == "tela_2":
    st.title("🔐 Área de Acesso")
    
    aba_login, aba_cadastro = st.tabs(["Já tenho conta (Login)", "Quero me cadastrar"])
    
    # --- FLUXO DE LOGIN ---
    with aba_login:
        st.subheader("Identifique-se para acessar")
        login_cpf = st.text_input("Digite seu CPF (apenas números)", key="input_login_cpf")
        login_senha = st.text_input("Digite sua Senha", type="password", key="input_login_senha")
        
        if st.button("Entrar no Sistema", type="primary"):
            if login_cpf in st.session_state.usuarios_cadastrados:
                usuario = st.session_state.usuarios_cadastrados[login_cpf]
                
                # Validação da Tela 5: Verifica se o administrador já aceitou o cliente
                if usuario["status"] == "Pendente":
                    st.warning("⚠️ Seu cadastro foi recebido, mas ainda precisa do aceite do Administrador (Tela 5).")
                elif usuario["senha"] == login_senha:
                    st.session_state.usuario_logado = login_cpf
                    st.success(f"Bem-vindo(a), {usuario['nome']}!")
                    time.sleep(1)
                    navegar_para("tela_3")
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
            if not (cad_nome and cad_cpf and cad_tel and cad_cep and cad_email and cad_senha):
                st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
            elif cad_cpf in st.session_state.usuarios_cadastrados:
                st.warning("⚠️ Este CPF já está registrado em nossa base.")
            else:
                st.session_state.usuarios_cadastrados[cad_cpf] = {
                    "nome": cad_nome,
                    "cpf": cad_cpf,
                    "telefone": cad_tel,
                    "cep": cad_cep,
                    "email": cad_email,
                    "senha": cad_senha,
                    "status": "Pendente",  # Começa pendente para aprovação do admin
                    "saldo": 0.0,
                    "plano_ativo": "Nenhum"
                }
                st.success("✅ Cadastro realizado! Aguarde o aceite do administrador no painel para conseguir logar.")
                
    st.markdown("---")
    if st.button("← Voltar para a Tela Inicial"):
        navegar_para("tela_1")


# ==========================================
# TELA 3: INFORMA OS APORTES / SAQUES
# ==========================================
elif st.session_state.tela_atual == "tela_3":
    cpf = st.session_state.usuario_logado
    user = st.session_state.usuarios_cadastrados[cpf]
    
    st.title("📥 Painel do Investidor")
    st.subheader(f"Seja bem-vindo, {user['nome']}.")
    
    # Mostra dados financeiros atuais do cliente
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="💰 Seu Saldo Disponível", value=f"R$ {user['saldo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col_s2:
        st.metric(label="📌 Plano Ativo", value=user['plano_ativo'])
        
    st.markdown("---")
    
    tab_fazer_aporte, tab_solicitar_saque = st.tabs(["Fazer Novo Aporte", "Solicitar Saque (Resgate)"])
    
    with tab_fazer_aporte:
        st.write("Selecione abaixo o valor do plano que deseja aportar:")
        for nome_plano, valor_plano in PLANOS.items():
            col_info, col_botao = st.columns()
            with col_info:
                st.write(f"🔹 **Plano {nome_plano}** — Valor único de Investimento:")
                st.subheader(f"R$ {valor_plano:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            with col_botao:
                st.write("") 
                if st.button(f"Escolher {nome_plano}", key=f"btn_{nome_plano}", type="primary"):
                    st.session_state.plano_selecionado = nome_plano
                    st.session_state.valor_selecionado = valor_plano
                    navegar_para("tela_4")
            st.markdown("---")
            
    with tab_solicitar_saque:
        st.write("Retire os lucros acumulados na sua conta:")
        if user["saldo"] <= 0:
            st.warning("Você ainda não possui saldo disponível para realizar saques.")
        else:
            valor_saque = st.number_input("Digite o valor que deseja sacar (R$)", min_value=1.0, max_value=user["saldo"], step=50.0)
            chave_pix_saque = st.text_input("Informe sua Chave PIX para o recebimento")
            
            if st.button("Confirmar Pedido de Saque", type="primary"):
                if not chave_pix_saque:
                    st.error("Por favor, digite uma chave PIX válida.")
                else:
                    # Envia a solicitação para a Tela 7 do admin
                    st.session_state.historico_saques.append({
                        "id_saque": len(st.session_state.historico_saques) + 1,
                        "cpf": cpf,
                        "nome": user["nome"],
                        "valor": valor_saque,
                        "chave_pix": chave_pix_saque,
                        "status": "Pendente"
                    })
                    st.success("✅ Solicitação de saque enviada! Aguardando autorização do administrador.")
                    time.sleep(2)
                    st.rerun()
        
    if st.button("← Sair / Fazer Logout"):
        st.session_state.usuario_logado = None
        navegar_para("tela_1")


# ==========================================
# TELA 4: TELA DE PAGAMENTO VIA PIX
# ==========================================
elif st.session_state.tela_atual == "tela_4":
    st.title("💸 Pagamento do Aporte")
    
    plano = st.session_state.plano_selecionado
    valor = st.session_state.valor_selecionado
    cpf_cliente = st.session_state.usuario_logado
    nome_cliente = st.session_state.usuarios_cadastrados[cpf_cliente]["nome"]
    
    st.subheader(f"Você escolheu o plano **{plano}**")
    st.info(f"Valor a pagar: **R$ {valor:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.write("Escaneie o QR Code abaixo pelo aplicativo do seu banco ou utilize a chave Copia e Cola:")
    st.image("https://qrserver.com", width=250)
    
    chave_copia_cola = f"00020101021126330014br.gov.bcb.pix0111123456789015204000053039865405{int(valor)}005802BR5913SISTEMA_APORT6009SAO_PAULO62070503***6304"
    st.text_area("Chave Pix Copia e Cola:", value=chave_copia_cola, height=90)
    st.markdown("---")
    
    if st.button("Confirmar que realizei o pagamento", type="primary", use_container_width=True):
        # Envia a intenção de aporte para a Tela 6 do admin
        st.session_state.historico_aportes.append({
            "id_aporte": len(st.session_state.historico_aportes) + 1,
            "cpf": cpf_cliente,
            "nome": nome_cliente,
            "plano": plano,
            "valor": valor,
            "status": "Pendente"
        })
        st.success("✅ Notificação de pagamento enviada! O administrador irá conferir e liberar no painel.")
        time.sleep(3)navegar_para("tela_3")
        if st.button("← Mudar de Plano"):navegar_para("tela_3")==========================================PAINEL DO ADMINISTRADOR 
        (TELAS 5, 6 e 7)==========================================elif st.session_state.tela_atual == "tela_admin":st.title
        ("🛠️ Painel Administrativo Geral")st.write("Gerencie os acessos, valide pagamentos e autorize os saques dos investidores.")
        if st.button("← Voltar para a Home Principal"):navegar_para("tela_1")st.markdown("---")# 
Divisão das funções administrativas requisitadas em abas dedicadasaba_tela5, aba_tela6, aba_tela7 = st.tabs(["👥 Tela 5: Aceite de Cadastros","💰 Tela 6: Autorizar Aportes (PIX)","💳 Tela 7: Autorizar Pedidos de Saque"])# ------------------------------------------# TELA 5 - Visualiza Cadastros e Dá Aceite# ------------------------------------------with aba_tela5:st.subheader("Novos clientes aguardando autorização de acesso")clientes_pendentes = [u for u in st.session_state.usuarios_cadastrados.values() if u["status"] == "Pendente"]if not clientes_pendentes:st.info("Não há nenhum novo cadastro pendente de aprovação.")else:for cliente in clientes_pendentes:with st.expander(f"📋 Cadastro de: {cliente['nome']}"):st.write(f"CPF: {cliente['cpf']}")st.write(f"E-mail: {cliente['email']} | Telefone: {cliente['telefone']}")st.write(f"CEP: {cliente['cep']}")if st.button(f"Dar Aceite / Aprovar {cliente['nome']}", key=f"aceite_{cliente['cpf']}", type="primary"):st.session_state.usuarios_cadastrados[cliente['cpf']]["status"] = "Aprovado"st.success(f"O acesso do cliente {cliente['nome']} foi liberado!")time.sleep(1)st.rerun()# ------------------------------------------# TELA 6 - Visualiza Aportes e Dá Autorização# ------------------------------------------with aba_tela6:st.subheader("Comprovantes e Aportes solicitados por PIX")aportes_pendentes = [a for a in st.session_state.historico_aportes if a["status"] == "Pendente"]if not aportes_pendentes:st.info("Nenhum pagamento PIX pendente de validação.")else:for ap in aportes_pendentes:with st.expander(f"💸 Aporte #{ap['id_aporte']} - Solicitado por: {ap['nome']}"):st.write(f"Plano Escolhido: {ap['plano']} | Valor: R$ {ap['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))st.write(f"CPF do Investidor: {ap['cpf']}")if st.button(f"Confirmar Recebimento e Ativar Plano", key=f"conf_ap_{ap['id_aporte']}", type="primary"):# Atualiza o status do investimentoap["status"] = "Aprovado"# Soma o valor investido ao saldo real do investidorst.session_state.usuarios_cadastrados[ap['cpf']]["saldo"] += ap['valor']st.session_state.usuarios_cadastrados[ap['cpf']]["plano_ativo"] = ap['plano']st.success("Pagamento homologado! Saldo inserido na conta do investidor.")time.sleep(1)st.rerun()# ------------------------------------------# TELA 7 - Autoriza os Pedidos de Saque# ------------------------------------------with aba_tela7:st.subheader("Pedidos de Resgate de Lucros efetuados pelos clientes")saques_pendentes = [s for s in st.session_state.historico_saques if s["status"] == "Pendente"]if not saques_pendentes:st.info("Não existem saques aguardando autorização financeira.")else:for sq in saques_pendentes:with st.expander(f"💳 Saque #{sq['id_saque']} - Solicitado por: {sq['nome']}"):st.write(f"Valor Solicitado: R$ {sq['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))st.write(f"Enviar PIX para a Chave: {sq['chave_pix']}")st.write(f"CPF do Destinatário: {sq['cpf']}")if st.button(f"Autorizar e Liquidar Saque", key=f"conf_sq_{sq['id_saque']}", type="primary"):# Muda o status do saquesq["status"] = "Concluído"# Deduz de forma real o dinheiro do saldo do clientest.session_state.usuarios_cadastrados[sq['cpf']]["saldo"] -= sq['valor']st.success("Saque autorizado! O valor foi debitado do saldo do investidor.")time.sleep(1)st.rerun()

