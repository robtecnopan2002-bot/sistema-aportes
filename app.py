import streamlit as st
import time
import banco

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
            # 1. Limpeza e padronização dos dados numéricos
            cpf_limpo = "".join(filter(str.isdigit, cad_cpf))
            tel_limpo = "".join(filter(str.isdigit, cad_tel))
            cep_limpo = "".join(filter(str.isdigit, cad_cep))

            # 2. Verificação individual e detalhada de cada campo (Passo 4 - UX)
            if not cad_nome.strip():
                st.error("⚠️ O campo **Nome Completo** não pode ficar vazio.")
                
            elif len(cpf_limpo) != 11:
                st.error(f"❌ Erro no campo **CPF**: Você digitou {len(cpf_limpo)} números. O CPF deve conter exatamente 11 dígitos numéricos.")
                
            elif len(tel_limpo) < 10 or len(tel_limpo) > 11:
                st.error(f"❌ Erro no campo **Telefone**: Formato inválido. Insira o DDD + número com 10 ou 11 dígitos (Ex: 11999998888).")
                
            elif len(cep_limpo) != 8:
                st.error(f"❌ Erro no campo **CEP**: Você informou {len(cep_limpo)} números. O CEP precisa ter exatamente 8 dígitos.")
                
            elif not st.session_state.end_salvo:
                st.error("⚠️ O campo **Endereço** precisa ser preenchido (busque pelo CEP ou use a opção manual).")
                
            elif not cad_email.strip() or "@" not in cad_email or "." not in cad_email.split("@")[-1]:
                st.error("❌ Erro no campo **E-mail**: O formato digitado é inválido. Certifique-se de usar um e-mail real (Ex: nome@provedor.com).")
                
            elif len(cad_senha) < 6:
                st.error(f"❌ Erro no campo **Senha**: Sua senha possui apenas {len(cad_senha)} caracteres. Crie uma senha mais segura com no mínimo 6 dígitos.")
                
            else:
                # Se tudo estiver perfeito, salva usando o endereço completo estruturado
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
    # CORREÇÃO DEFINITIVA: Atualiza e unifica a busca do usuário logado no banco
    user = banco.obter_usuario(cpf)
    usuario = user
    user_cliente = user
    st.title("📥 Painel do Aportador")
  
    st.subheader(f"Seja bem-vindo(a), {user[0] if isinstance(user, (list, tuple)) else user.get('nome', '')}.")
    
    # --- MOTOR DE EXTRAÇÃO SEGURO DE DADOS ---
    if isinstance(user, dict):
        v_saldo = float(user.get('saldo', 0.0))
        v_rend = float(user.get('rendimento', 0.0))
        v_plano = str(user.get('plano_active', user.get('plano_ativo', 'Nenhum')))
    elif isinstance(user, (list, tuple)):
        # Fallback para leitura direta por índices caso o Row Factory falhe no servidor
        v_saldo = float(user[6]) if len(user) > 6 else 0.0
        v_rend = float(user[9]) if len(user) > 9 else 0.0
        v_plano = str(user[8]) if len(user) > 8 else "Nenhum"
    else:
        v_saldo, v_rend, v_plano = 0.0, 0.0, "Nenhum"
    # ----------------------------------------

    # Exibição unificada com o rendimento somando direto no aporte
    if isinstance(user, dict):
        v_saldo = float(user.get('saldo', 0.0))
        v_plano = str(user.get('plano_active', user.get('plano_ativo', 'Nenhum')))
    elif isinstance(user, (list, tuple)):
        v_saldo = float(user[6]) if len(user) > 6 else 0.0
        v_plano = str(user[8]) if len(user) > 8 else "Nenhum"
    else:
        v_saldo, v_plano = 0.0, "Nenhum"

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="💰 Saldo Total Disponível (Com Rendimentos)", value=f"R$ {v_saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col_s2:
        st.metric(label="📌 Plano Ativo", value=v_plano)




        
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
            st.markdown(
                f"""
                <div style="background-color: #081F42; padding: 15px; border-radius: 8px; border-left: 5px solid #B59453; margin-bottom: 20px;">
                    <p style="margin: 0; color: #FFFFFF; font-size: 14px;">📋 <b>Regras de Resgate RCB:</b></p>
                    <ul style="margin: 5px 0 0 0; padding-left: 20px; color: #A0AEC0; font-size: 13px;">
                        <li>Saque imediato permitido apenas sobre o <b>Valor de Rendimento</b>.</li>
                        <li>O valor principal do aporte fica retido por <b>15 dias</b> ou depende de <b>autorização do administrador</b>.</li>
                    </ul>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if v_rend <= 0:
                st.info("👋 Seu rendimento disponível para saque imediato está zerado. Para resgatar o Capital Aportado antes do prazo, entre em contato com o suporte para solicitar a autorização do administrador.")
            else:
                valor_saque = st.number_input("Valor do saque (R$)", min_value=1.0, max_value=float(v_rend), step=10.0, key="num_saque_final_real")
                chave_pix_saque = st.text_input("Informe sua Chave PIX para recebimento:", key="txt_pix_saque_final_real")
                
                if st.button("Confirmar Pedido de Saque", type="primary", key="btn_confirmar_saque_real_final"):
                    if not chave_pix_saque.strip():
                        st.error("⚠️ Por favor, informe sua Chave PIX para continuar.")
                    else:
                        banco.solicitar_saque(cpf, user[0] if isinstance(user, (list, tuple)) else user.get('nome', ''), valor_saque, chave_pix_saque)
                        st.success(f"✅ Solicitação de saque de R$ {valor_saque:,.2f} enviada para processamento!")
                        import time; time.sleep(1.5); st.rerun()



        
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
    
    # 1. GERADOR DINÂMICO DE PIX DA SUA CONTA (Calculado Primeiro)
    minha_chave_real = st.secrets.get("CHAVE_PIX_RECEBIMENTO", "robtecnopan2004@gmail.com")
    tamanho_chave = f"{len(minha_chave_real):02d}"
    valor_formatado = f"{valor:.2f}"
    tamanho_valor = f"{len(valor_formatado):02d}"
    
    chave_copia_cola = f"00020101021126330014br.gov.bcb.pix01{tamanho_chave}{minha_chave_real}52040000530398654{tamanho_valor}{valor_formatado}5802BR5911RCB_APORTES6009SAO_PAULO62070503***6304"
    
    # 2. EXIBIÇÃO DOS TEXTOS E COMPONENTES VISUAIS
    st.subheader(f"Você escolheu o plano **{plano}**")
    st.info(f"Valor a pagar: **R$ {valor:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
    st.write("Escaneie o QR Code abaixo usando o aplicativo do seu banco:")
    
    # 3. GERADOR INTERNO DE QR CODE REAL (PASSO 4 - BLINDADO)
    import qrcode
    from io import BytesIO
    
    try:
        # Cria o objeto do QR Code com o texto dinâmico do Pix
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(chave_copia_cola)
        qr.make(fit=True)
        
        # Transforma o desenho em bytes de imagem na memória do servidor
        img_qr = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        
        # Desenha a imagem na tela de forma direta e segura
        st.image(buffer.getvalue(), width=250)
    except Exception:
        st.warning("⚠️ Aguardando geração do QR Code...")

    
    st.text_area("Chave Pix Copia e Cola (Clique para copiar e pagar):", value=chave_copia_cola, height=90)
    st.markdown("---")


    
    # --- GERADOR DINÂMICO DE PIX DA SUA CONTA (PASSO 4) ---
    minha_chave_real = st.secrets.get("CHAVE_PIX_RECEBIMENTO", "suachave@exemplo.com")
    
    # Monta a estrutura oficial do PIX de acordo com o padrão do Banco Central
    tamanho_chave = f"{len(minha_chave_real):02d}"
    valor_formatado = f"{valor:.2f}"
    tamanho_valor = f"{len(valor_formatado):02d}"
    
    # String dinâmica contendo a sua conta, o valor exato do plano e o nome identificador
if st.session_state.tela_atual == "tela_4":
    st.text_area("Chave Pix Copia e Cola (Clique para copiar e pagar):", value=chave_copia_cola, height=90, key="pix_copia_cola_final")
    st.markdown("---")
    if st.button("Confirmar que realizei o pagamento", type="primary", use_container_width=True, key="btn_confirmar_pgto"):
        banco.solicitar_aporte(cpf_cliente, nome_cliente, plano, valor)
        st.success("✅ Notificação de pagamento enviada!")
        import time
        time.sleep(2)
        navegar_para("tela_3")
    if st.button("← Mudar de Plano", key="btn_mudar_plano_pgto"):
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
                    st.success("Acesso liberado!")
                    st.rerun()
                else:
                    st.error("Senha incorreta.")

    # Se o administrador já estiver logado, exibe o painel com os dados novos
    if st.session_state.admin_logado:
        st.subheader("👥 Solicitações de Cadastro Pendentes")
        
        # Busca a lista completa de usuários pendentes no banco
        usuarios_pendentes = banco.listar_usuarios_pendentes() if hasattr(banco, 'listar_usuarios_pendentes') else []
        
        if not usuarios_pendentes:
            st.info("Não há novos cadastros aguardando aprovação no momento.")
        
        else:
            st.markdown("### 📋 Novos clientes aguardando autorização")
            
            for usr in usuarios_pendentes:
                with st.container():
                    # Nome principal do cliente aguardando
                    st.markdown(f"**👤 Cliente: {usr.get('nome', 'Não informado')}**")
                    
                    # Dados secundários em formato menor e compacto (Passo 4 - UX)
                    texto_detalhes = f"""
                    <div style='line-height: 1.4; margin-top: -5px; margin-bottom: 10px;'>
                        <small style='color: #A0AEC0;'>
                            <b>CPF:</b> {usr.get('cpf', '-')} | 
                            <b>Telefone:</b> {usr.get('telefone', '-')} <br>
                            <b>E-mail:</b> {usr.get('email', '-')} | 
                            <b>CEP:</b> {usr.get('cep', '-')}
                        </small>
                    </div>
                    """
                    st.markdown(texto_detalhes, unsafe_allow_html=True)
                    
                    # Criando chaves de controle na memória para a caixa de motivo de recusa
                    chave_recusa = f"escrever_recusa_{usr.get('cpf')}"
                    if chave_recusa not in st.session_state:
                        st.session_state[chave_recusa] = False

                    # Botões de ação alinhados lado a lado (Corrigido com proporção exata)
                    col_b1, col_b2, col_espaco = st.columns([2, 2, 6])
                    
                    with col_b1:
                        if st.button("✔️ Aceitar", key=f"ac_{usr.get('cpf')}", type="primary", use_container_width=True):
                            if hasattr(banco, 'aprovar_usuario'):
                                # Executa a aprovação padrão do cliente
                                banco.aprovar_usuario(usr.get('cpf'))
                                
                                # INTERVENÇÃO DO PASSO 4: Força a coluna rendimento a iniciar como número 0.0 puro
                                if hasattr(banco, 'atualizar_rendimento'):
                                    banco.atualizar_rendimento(usr.get('cpf'), 0.0)
                                    
                                st.success("Aprovado com contabilidade limpa!")
                                st.rerun()

                    with col_b2:
                        if st.button("❌ Recusar", key=f"rc_{usr.get('cpf')}", use_container_width=True):
                            st.session_state[chave_recusa] = True  # Ativa a caixa de texto na tela

                    # Se o botão recusar for clicado, abre a caixa de mensagem personalizada (Passo 4 - UX)
                    if st.session_state[chave_recusa]:
                        st.markdown("<br>", unsafe_allow_html=True)
                        motivo_email = st.text_area(
                            f"Escreva o motivo da recusa para {usr.get('nome')} (Será enviado ao e-mail: {usr.get('email')}):",
                            key=f"txt_motivo_{usr.get('cpf')}",
                            placeholder="Ex: Prezado cliente, seu cadastro foi recusado pois o comprovante anexado está ilegível. Por favor, refaça o envio."
                        )
                        
                        col_env1, col_env2 = st.columns(2)
                        with col_env1:
                            if st.button("✉️ Confirmar e Enviar E-mail", key=f"conf_rc_{usr.get('cpf')}", type="primary"):
                                if not motivo_email.strip():
                                    st.error("⚠️ Você precisa escrever o motivo antes de confirmar.")
                                else:
                                    # Tenta enviar o e-mail em segundo plano de forma isolada
                                    try:
                                        import urllib.request
                                        import json
                                        
                                        # Verifica de forma segura se a chave existe nos Secrets antes de rodar
                                        chave_api = st.secrets.get("CHAVE_BREVO", "xkeysib-PROVISORIO_MUTAVEL_TESTE")
                                        
                                        url_email = "https://brevo.com"
                                        payload_dados = {
                                            "sender": {"name": "RCB Aportes", "email": "onboarding@rcbaportes.com"},
                                            "to": [{"email": usr.get('email'), "name": usr.get('nome')}],
                                            "subject": "RCB Aportes - Atualização do Status de Cadastro",
                                            "textContent": f"Prezado(a) {usr.get('nome')},\n\nInformamos que seu pedido de cadastro no sistema RCB Aportes não pôde ser aprovado neste momento pelo seguinte motivo:\n\n{motivo_email}\n\nAtenciosamente,\nEquipe de Suporte RCB Aportes"
                                        }
                                        
                                        req_email = urllib.request.Request(url_email, data=json.dumps(payload_dados).encode('utf-8'))
                                        req_email.add_header('api-key', chave_api)
                                        req_email.add_header('Content-Type', 'application/json')
                                        req_email.add_header('Accept', 'application/json')
                                        
                                        with urllib.request.urlopen(req_email, timeout=3) as resposta:
                                            pass
                                    except Exception:
                                        # Se der erro no e-mail, o Python engole a falha e avança para não quebrar a tela
                                        pass
                                    
                                    # Executa a ação principal no banco de dados com estabilidade garantida
                                    if hasattr(banco, 'reprovar_usuario'):
                                        banco.reprovar_usuario(usr.get('cpf'))
                                        
                                    st.session_state[chave_recusa] = False
                                    st.success(f"✅ Cadastro de {usr.get('nome')} processado no painel!")
                                    st.button("🔄 Atualizar Lista", type="primary", key=f"btn_clear_{usr.get('cpf')}")


                        with col_env2:
                            if st.button("Cancelar", key=f"canc_rc_{usr.get('cpf')}"):
                                st.session_state[chave_recusa] = False
                                st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("⚙️ Gestão de Saldos e Liberação de Aportes")
        
        # Campo para o administrador digitar o CPF do cliente que deseja alterar
        cpf_gestao = st.text_input("Digite o CPF do cliente para gerenciar (Apenas números):", key="cpf_gestao_admin")
        
        if cpf_gestao:
            usuario_gestao = banco.obter_usuario(cpf_gestao)
            if usuario_gestao:
                st.write(f"👤 **Cliente:** {usuario_gestao['nome']} | **Plano Ativo:** {usuario_gestao.get('plano_ativo', 'Nenhum')}")
                
                # --- FORMULÁRIO 1: LANÇAMENTO DE RENDIMENTO (ISOLADO E BLINDADO) ---
                with st.form(key="form_lancar_rendimento_admin"):
                    st.write("📊 **Painel de Rendimentos**")
                    novo_rendimento = st.number_input("Adicionar Novo Rendimento Líquido (R$):", min_value=0.0, step=10.0, key="input_add_rend_real")
                    
                    if st.form_submit_button("📈 Confirmar e Lançar Rendimento", type="primary", use_container_width=True):
                        if novo_rendimento <= 0:
                            st.error("⚠️ Insira um valor maior que zero para lançar.")
                        else:
                            try:
                                # Força o disparo direto e engole qualquer delay do Streamlit
                                banco.injetar_lucro_cliente(cpf_gestao, novo_rendimento)
                                st.success(f"✅ Sucesso! R$ {novo_rendimento:,.2f} adicionados ao rendimento de {usuario_gestao['nome']}.")
                                import time; time.sleep(1.5); st.rerun()
                            except Exception as err:
                                st.error(f"Erro técnico ao gravar: {err}")

                st.markdown("<br>", unsafe_allow_html=True)

                # --- FORMULÁRIO 2: LIBERAÇÃO DE CAPITAL RETIDO (ISOLADO) ---
                with st.form(key="form_liberar_capital_admin"):
                    st.write("🔓 **Carência e Quebra de Retenção**")
                    max_liberar = float(usuario_gestao['saldo']) if usuario_gestao['saldo'] is not None else 0.0
                    valor_liberar = st.number_input("Liberar Capital Retido para Saque Imediato (R$):", min_value=0.0, max_value=max_liberar, step=50.0, key="input_lib_cap_real")
                    
                    if st.form_submit_button("🔓 Autorizar Saque do Aporte", use_container_width=True):
                        if valor_liberar <= 0:
                            st.error("⚠️ Insira un valor maior que zero.")
                        else:
                            try:
                                banco.processar_liberacao_aporte(cpf_gestao, valor_liberar)
                                st.success(f"✅ Sucesso! R$ {valor_liberar:,.2f} transferidos para área livre.")
                                import time; time.sleep(1.5); st.rerun()
                            except Exception as err:
                                st.error(f"Erro técnico ao liberar: {err}")


                
                with col_g2:
                    # Permite ao administrador liberar o capital retido transformando-o em rendimento sacável
                    valor_liberar = st.number_input("Liberar Capital Retido para Saque (R$):", min_value=0.0, max_value=float(usuario_gestao['saldo']), step=50.0, key="lib_cap")
                    if st.button("🔓 Autorizar Saque do Aporte", use_container_width=True, key="btn_autorizar_saque"):
                        if hasattr(banco, 'atualizar_saldos_liberacao'):
                            # Remove do saldo retido e joga para o rendimento liberado
                            banco.atualizar_saldos_liberacao(cpf_gestao, valor_liberar)
                            st.success("Capital liberado para saque imediato!")
                            import time; time.sleep(1.5); st.rerun()
            else:
                st.error("CPF não localizado no sistema.")
        
        if st.button("← Sair do Painel Admin"):
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
