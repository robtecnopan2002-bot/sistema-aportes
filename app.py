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

SENHA_MESTRE_ADMIN = "admin993412"

PLANOS = {
    "Cobre": 300.00,
    "Bronze": 600.00,
    "Prata": 1000.00,
    "Ouro": 3000.00,
    "Diamante": 5000.00
}
# --- PASSO 4: IDENTIDADE VISUAL RCB APORTES ---
st.markdown(
    """
        <style>
    .stApp { background-color: #031430; }
    .titulo-logo { font-family: 'Georgia', serif; font-size: 46px; font-weight: bold; color: #FFFFFF; margin-bottom: 0px; }
    .subtitulo-logo { font-family: 'Arial', sans-serif; font-size: 16px; font-weight: bold; color: #B59453; letter-spacing: 4px; margin-top: -10px; margin-bottom: 30px; }
    div.stButton > button:first-child { background-color: #B59453; color: #031430; font-weight: bold; border-radius: 8px; border: none; }
    div.stButton > button:first-child:hover { background-color: #94763E; color: #FFFFFF; border: none; }
    
    /* NOVA REGRA: Força todos os textos normais, parágrafos e subtítulos a ficarem brancos */
    .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label {
        color: #FFFFFF !important;
    }
    </style>

    """,
    unsafe_allow_html=True
)
def navegar_para(nova_tela):
    st.session_state.tela_atual = nova_tela
    st.rerun()

# --- TELA 1: VISUALIZAÇÃO DO PRODUTO ---
if st.session_state.tela_atual == "tela_1":
    # Adiciona o logotipo oficial da RCB centralizado na tela
    st.image("Logo RCB Investimentos (4).jpg", width=350)
    
    st.subheader("Multiplique seu capital diariamente")


    st.markdown("---")
    st.metric(label="📊 Lucros Diários Estimados", value="1,0% a 5,0% ao dia")
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
            # NOVO: Consulta o banco de dados real
            usuario = banco.obter_usuario(login_cpf)
            if usuario:
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
        
        # --- BLOCO DE ENDEREÇO SEPARADO EM CAMPOS (PASSO 4) ---
        cad_cep = st.text_input("CEP (Apenas números)", key="reg_cep")
        
        if "end_salvo" not in st.session_state:
            st.session_state.end_salvo = ""
            
        # Botões de controle visual
        col_cep1, col_cep2 = st.columns(2)
        with col_cep1:
            if st.button("🔍 Buscar Endereço Automático", type="secondary", use_container_width=True):
                cep_limpo_busca = "".join(filter(str.isdigit, cad_cep))
                if len(cep_limpo_busca) == 8:
                    import urllib.request
                    import json
                    try:
                        url = f"https://awesomeapi.com.br{cep_limpo_busca}"
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=4) as response:
                            dados_cep = json.loads(response.read().decode())
                        st.session_state.end_salvo = f"{dados_cep.get('address', '')}, {dados_cep.get('district', '')} - {dados_cep.get('city', '')}/{dados_cep.get('state', '')}"
                    except Exception:
                        st.session_state.end_salvo = "Liberar Campos"
                else:
                    st.error("Digite 8 números.")
        
        with col_cep2:
            if st.button("✏️ Preencher Manualmente", type="secondary", use_container_width=True):
                st.session_state.end_salvo = "Liberar Campos"

        # Se a busca automática falhar ou o usuário clicar em manual, abre os campos separados
        if st.session_state.end_salvo == "Liberar Campos" or not st.session_state.end_salvo:
            col_end1, col_end2 = st.columns([3, 1])
            with col_end1:
                end_rua = st.text_input("Rua / Avenida:", key="input_rua")
            with col_end2:
                end_num = st.text_input("Número:", key="input_num")
                
            col_end3, col_end4 = st.columns(2)
            with col_end3:
                end_bairro = st.text_input("Bairro:", key="input_bairro")
            with col_end4:
                end_cidade = st.text_input("Cidade / Estado:", key="input_cidade")
            
            # Junta as partes em uma única variável se todas forem preenchidas
            if end_rua and end_num and end_bairro and end_cidade:
                st.session_state.end_salvo = f"{end_rua}, {end_num} - {end_bairro}, {end_cidade}"
        
        elif st.session_state.end_salvo and st.session_state.end_salvo != "Liberar Campos":
            st.success(f"📍 **Endereço Localizado:** {st.session_state.end_salvo}")
        # -------------------------------------------------------




             
        cad_email = st.text_input("E-mail", key="reg_email")
        cad_senha = st.text_input("Crie uma Senha", type="password", key="reg_senha")

        if st.button("Finalizar Meu Cadastro", type="secondary"):
            cpf_limpo = "".join(filter(str.isdigit, cad_cpf))
            tel_limpo = "".join(filter(str.isdigit, cad_tel))
            cep_limpo = "".join(filter(str.isdigit, cad_cep))
            if not (cad_nome and cad_cpf and cad_tel and cad_cep and cad_email and cad_senha):
                st.error("⚠️ Preencha todos os campos obrigatórios.")
            elif len(cpf_limpo) != 11:
                st.error("❌ CPF inválido. O campo deve conter exatamente 11 números.")
            elif len(tel_limpo) < 10 or len(tel_limpo) > 11:
                st.error("❌ Telefone inválido. Insira o DDD + número (ex: 11999999999).")
            elif len(cep_limpo) != 8:
                st.error("❌ CEP inválido. O campo deve conter exatamente 8 números.")
            elif "@" not in cad_email or "." not in cad_email.split("@")[-1]:
                st.error("❌ E-mail inválido. Digite um formato correto (ex: nome@email.com).")
            elif len(cad_senha) < 6:
                st.error("❌ Senha muito curta. Crie uma senha com no mínimo 6 caracteres.")
            else:
                sucesso = banco.cadastrar_usuario(cad_nome, cpf_limpo, tel_limpo, cep_limpo, cad_email, cad_senha)
                if sucesso:
                    st.success("✅ Cadastro realizado com sucesso! Aguarde o aceite do administrador no painel.")
                else:
                    st.warning("⚠️ Este CPF já está registrado no sistema.")



                
    st.markdown("---")
    if st.button("← Voltar para a Tela Inicial"):
        navegar_para("tela_1")

# --- TELA 3: PAINEL DO APORTADOR ---
elif st.session_state.tela_atual == "tela_3":
    cpf = st.session_state.usuario_logado
    # NOVO: Busca dados atualizados do banco
    user = banco.obter_usuario(cpf)
    st.title("📥 Painel do Aportador")
    st.subheader(f"Seja bem-vindo(a), {user['nome']}.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="💰 Saldo Total Aportado", value=f"R$ {user['saldo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col_s2:
        st.metric(label="📌 Plano de Aporte Ativo", value=user['plano_active'] if 'plano_active' in user else user.get('plano_ativo', 'Nenhum'))

        
    st.markdown("---")
    tab_fazer_aporte, tab_solicitar_saque = st.tabs(["Fazer Novo Aporte", "Solicitar Saque (Resgate)"])
    
    with tab_fazer_aporte:
        for nome_plano, valor_plano in PLANOS.items():
            col_info, col_botao = st.columns(2)
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
                    # NOVO: Registra o pedido de saque no banco
                    banco.solicitar_saque(cpf, user["nome"], valor_saque, chave_pix_saque)
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
    user_cliente = banco.obter_usuario(cpf_cliente)
    nome_cliente = user_cliente["nome"]
    
    st.subheader(f"Você escolheu o plano **{plano}**")
    st.info(f"Valor a pagar: **R$ {valor:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
    st.write("Escaneie o QR Code ou utilize a chave Copia e Cola:")
    st.image("https://qrserver.com", width=250)
    
    chave_copia_cola = f"00020101021126330014br.gov.bcb.pix0111123456789015204000053039865405{int(valor)}005802BR5913SISTEMA_APORT6009SAO_PAULO62070503***6304"
    st.text_area("Chave Pix Copia e Cola:", value=chave_copia_cola, height=90)
    st.markdown("---")
    
    if st.button("Confirmar que realizei o pagamento", type="primary", use_container_width=True):
        banco.solicitar_aporte(cpf_cliente, nome_cliente, plano, valor)
        st.success("✅ Notificação de pagamento enviada!")
        time.sleep(2)
        navegar_para("tela_3")
    if st.button("← Mudar de Plano"):
        navegar_para("tela_3")

# --- PAINEL DO ADMINISTRADOR (TELAS 5, 6 e 7 + RENDIMENTOS MANUAIS) ---
elif st.session_state.tela_atual == "tela_admin":
    st.title("🛠️ Painel Administrativo Geral")
    
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
                
    else:
        col_logout_admin1, col_logout_admin2 = st.columns(2)
        with col_logout_admin1:
            st.write("Gerencie os acessos, valide pagamentos e autorize os saques dos investidores.")
        with col_logout_admin2:
            if st.button("🔒 Sair do Painel Admin", type="secondary", use_container_width=True):
                st.session_state.admin_logado = False
                navegar_para("tela_1")
                
        st.markdown("---")
        aba_tela5, aba_tela6, aba_tela7, aba_rendimentos = st.tabs([
            "👥 Tela 5: Aceite de Cadastros", "💰 Tela 6: Autorizar Aportes", "💳 Tela 7: Autorizar Saques", "📈 Rendimentos Individuais"
        ])
        
        with aba_tela5:
            st.subheader("Novos clientes aguardando autorização")
            clientes_pendentes = banco.listar_usuarios_pendentes()
            if not clientes_pendentes:
                st.info("Nenhum cadastro pendente.")
            else:
                for cl in clientes_pendentes:
                    with st.expander(f"📋 Cadastro de: {cl['nome']}"):
                        st.write(f"**CPF:** {cl['cpf']} | **Tel:** {cl['telefone']} | **CEP:** {cl['cep']}")
                        if st.button(f"Aprovar {cl['nome']}", key=f"aceite_{cl['cpf']}", type="primary"):
                            banco.aprovar_usuario(cl['cpf'])
                            st.success("Cliente liberado!")
                            time.sleep(1)
                            st.rerun()

        with aba_tela6:
            st.subheader("Aportes solicitados por PIX")
            aportes_pendentes = banco.listar_aportes_pendentes()
            if not aportes_pendentes:
                st.info("Nenhum pagamento pendente.")
            else:
                for ap in aportes_pendentes:
                    with st.expander(f"💸 Aporte #{ap['id_aporte']} - {ap['nome']}"):
                        st.write(f"**Plano:** {ap['plano']} | **Valor:** R$ {ap['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                        if st.button(f"Confirmar PIX", key=f"conf_ap_{ap['id_aporte']}", type="primary"):
                            banco.aprovar_aporte(ap['id_aporte'], ap['cpf'], ap['valor'], ap['plano'])
                            st.success("Saldo inserido!")
                            time.sleep(1)
                            st.rerun()

        with aba_tela7:
            st.subheader("Pedidos de Resgate de Lucros")
            saques_pendentes = banco.listar_saques_pendentes()
            if not saques_pendentes:
                st.info("Não existem saques aguardando autorização.")
            else:
                for sq in saques_pendentes:
                    with st.expander(f"💳 Saque #{sq['id_saque']} - {sq['nome']}"):
                        st.write(f"**Valor:** R$ {sq['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                        st.write(f"**Chave PIX:** {sq['chave_pix']}")
                        if st.button(f"Liquidar Saque", key=f"conf_sq_{sq['id_saque']}", type="primary"):
                            banco.aprovar_saque(sq['id_saque'], sq['cpf'], sq['valor'])
                            st.success("Saque autorizado e debitado!")
                            time.sleep(1)
                            st.rerun()

        # MODIFICADO: Lançamento manual por investidor
        with aba_rendimentos:
            st.subheader("Lançamento Manual de Rendimentos")
            st.write("Selecione o investidor na lista abaixo e informe a porcentagem de lucro a ser aplicada sobre o saldo dele.")
            
            usuarios_ativos = banco.listar_usuarios_ativos()
            
            if not usuarios_ativos:
                st.info("Nenhum investidor ativo e aprovado com saldo no momento.")
            else:
                for usr in usuarios_ativos:
                    saldo_formatado = f"R$ {usr['saldo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    with st.expander(f"👤 {usr['nome']} (Plano: {usr['plano_ativo']} | Saldo Atual: {saldo_formatado})"):
                        st.write(f"**CPF:** {usr['cpf']}")
                        
                        # Campo numérico para digitar a taxa de lucro de 0.1% a 1.0% (ou mais se desejar)
                        taxa_manual = st.number_input(
                            f"Porcentagem de Rendimento para {usr['nome']} (%)",
                            min_value=0.01,
                            max_value=10.0,
                            value=0.5,
                            step=0.01,
                            key=f"taxa_{usr['cpf']}"
                        )
                        
                        if st.button(f"Lançar Rendimento para {usr['nome']}", key=f"btn_rend_{usr['cpf']}", type="primary"):
                            banco.aplicar_rendimento_manual(usr['cpf'], taxa_manual)
                            st.success(f"🎉 Sucesso! Rendimento de {taxa_manual}% aplicado ao saldo de {usr['nome']}!")
                            time.sleep(1.5)
                            st.rerun()
