import sqlite3

# ALTERAÇÃO DO PASSO 4: Força a nuvem a criar um banco totalmente novo e limpo
DB_NAME = "sistema_v2.db"


def conectar():
    """Conecta ao banco de dados SQLite e corrige saldos nulos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Preenche com 0.0 qualquer conta antiga que esteja com o rendimento nulo/vazio
        cursor.execute("UPDATE usuarios SET rendimento = 0.0 WHERE rendimento IS NULL;")
        conn.commit()
    except Exception:
        pass
    return conn


def inicializar_banco():
    """Cria as tabelas necessárias se elas não existirem."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabela de Usuários (Tela 2)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            telefone TEXT,
            cep TEXT,
            email TEXT,
            senha TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente',
            saldo REAL DEFAULT 0.0,
            plano_ativo TEXT DEFAULT 'Nenhum'
        )
    """)
    
    # Tabela de Aportes (Telas 4 e 6)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT,
            nome TEXT,
            plano TEXT,
            valor REAL,
            status TEXT DEFAULT 'Pendente',
            FOREIGN KEY (cpf) REFERENCES usuarios (cpf)
        )
    """)
    
    # Tabela de Saques (Telas 3 e 7)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT,
            nome TEXT,
            valor REAL,
            chave_pix TEXT,
            status TEXT DEFAULT 'Pendente',
            FOREIGN KEY (cpf) REFERENCES usuarios (cpf)
        )
    """)
    
    conn.commit()
    conn.close()

# --- FUNÇÕES DE USUÁRIOS ---
def cadastrar_usuario(nome, cpf, telefone, cep, email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, cpf, telefone, cep, email, senha, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Pendente')
        """, (nome, cpf, telefone, cep, email, senha))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # CPF já existe

def obter_usuario(cpf):
    conn = conectar()
    # Ativa o mapeamento oficial por nomes de colunas
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. Garante que a coluna rendimento exista antes de fazer a busca
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN rendimento REAL DEFAULT 0.0;")
        conn.commit()
    except Exception:
        pass

    # 2. Faz a busca geral na tabela de usuários
    cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
    linha = cursor.fetchone()
    conn.close()
    
    if linha:
        # Transforma o retorno em um dicionário puro do Python
        dados = dict(linha)
        
        # Converte os saldos para números reais de forma garantida
        saldo_limpo = float(dados.get("saldo", 0.0) if dados.get("saldo") is not None else 0.0)
        rend_limpo = float(dados.get("rendimento", 0.0) if dados.get("rendimento") is not None else 0.0)
        
        return {
            "nome": str(dados.get("nome", "")),
            "cpf": str(dados.get("cpf", "")),
            "telefone": str(dados.get("telefone", "")),
            "cep": str(dados.get("cep", "")),
            "email": str(dados.get("email", "")),
            "senha": str(dados.get("senha", "")),
            "saldo": saldo_limpo,
            "status": str(dados.get("status", "")),
            "plano_ativo": str(dados.get("plano_ativo", "Nenhum")),
            "rendimento": rend_limpo
        }
    return None



def listar_usuarios_pendentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, telefone, cep, email FROM usuarios WHERE status = 'Pendente'")
    rows = cursor.fetchall()
    conn.close()
    return [{"nome": r[0], "cpf": r[1], "telefone": r[2], "cep": r[3], "email": r[4]} for r in rows]

def aprovar_usuario(cpf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET status = 'Aprovado' WHERE cpf = ?", (cpf,))
    conn.commit()
    conn.close()

# --- FUNÇÕES DE APORTES ---
def solicitar_aporte(cpf, nome, plano, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aportes (cpf, nome, plano, valor, status)
        VALUES (?, ?, ?, ?, 'Pendente')
    """, (cpf, nome, plano, valor))
    conn.commit()
    conn.close()

def listar_aportes_pendentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cpf, nome, plano, valor FROM aportes WHERE status = 'Pendente'")
    rows = cursor.fetchall()
    conn.close()
    return [{"id_aporte": r[0], "cpf": r[1], "nome": r[2], "plano": r[3], "valor": r[4]} for r in rows]

def aprovar_aporte(id_aporte, cpf, valor, plano):
    conn = conectar()
    cursor = conn.cursor()
    # Atualiza o aporte para aprovado
    cursor.execute("UPDATE aportes SET status = 'Aprovado' WHERE id = ?", (id_aporte,))
    # Atualiza o saldo e o plano ativo do usuário
    cursor.execute("UPDATE usuarios SET saldo = saldo + ?, plano_ativo = ? WHERE cpf = ?", (valor, plano, cpf))
    conn.commit()
    conn.close()

# --- FUNÇÕES DE SAQUES ---
def solicitar_saque(cpf, nome, valor, chave_pix):
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Registra o pedido de saque na tabela de solicitações do administrador
    cursor.execute(
        "INSERT INTO saques (cpf_cliente, nome_cliente, valor, chave_pix, status, data_pedido) VALUES (?, ?, ?, ?, 'Pendente', datetime('now', 'localtime'))",
        (cpf, nome, valor, chave_pix)
    )
    
    # 2. Deduz o valor solicitado estritamente do Rendimento Líquido do cliente
    cursor.execute(
        "UPDATE usuarios SET rendimento = rendimento - ? WHERE cpf = ?",
        (valor, cpf)
    )
    
    conn.commit()
    conn.close()

def listar_saques_pendentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cpf, nome, valor, chave_pix FROM saques WHERE status = 'Pendente'")
    rows = cursor.fetchall()
    conn.close()
    return [{"id_saque": r[0], "cpf": r[1], "nome": r[2], "valor": r[3], "chave_pix": r[4]} for r in rows]

def aprovar_saque(id_saque, cpf, valor):
    conn = conectar()
    cursor = conn.cursor()
    # Atualiza o saque para concluído
    cursor.execute("UPDATE saques SET status = 'Concluído' WHERE id = ?", (id_saque,))
    # Deduz o valor do saldo do usuário
    cursor.execute("UPDATE usuarios SET saldo = saldo - ? WHERE cpf = ?", (valor, cpf))
    conn.commit()
    conn.close()

# Inicializa as tabelas automaticamente ao importar o arquivo
inicializar_banco()


def listar_usuarios_ativos():
    """Retorna a lista de todos os usuários aprovados e ativos no sistema."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, saldo, plano_ativo FROM usuarios WHERE status = 'Aprovado'")
    rows = cursor.fetchall()
    conn.close()
    return [{"nome": r[0], "cpf": r[1], "saldo": r[2], "plano_ativo": r[3]} for r in rows]

def aplicar_rendimento_manual(cpf, porcentagem):
    """Aplica o rendimento configurado manualmente para um usuário específico."""
    conn = conectar()
    cursor = conn.cursor()
    fator_multiplicador = 1 + (porcentagem / 100)
    cursor.execute("""
        UPDATE usuarios 
        SET saldo = saldo * ? 
        WHERE cpf = ?
    """, (fator_multiplicador, cpf))
    # --- ATUALIZAÇÃO AUTOMÁTICA DO PASSO 4 (ADICIONA COLUNA RENDIMENTO SE NÃO EXISTIR) ---
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN rendimento REAL DEFAULT 0.0;")
        conn.commit()
    except sqlite3.OperationalError:
        # Se a coluna já existir, o SQLite gera um erro amigável e o Python apenas ignora
        pass
    # ----------------------------------------------------------------------------------

def injetar_lucro_cliente(cpf, valor_lucro):
    """Soma o lucro exclusivamente na coluna rendimento do SQLite sem mexer no saldo."""
    conn = conectar()
    cursor = conn.cursor()
    # Puxa o rendimento atual para somar com o novo de forma matemática limpa
    cursor.execute("SELECT rendimento FROM usuarios WHERE cpf = ?", (cpf,))
    linha = cursor.fetchone()
    rend_atual = float(linha[0]) if linha and linha[0] is not None else 0.0
    
    # Executa o comando atualizando apenas o campo correto
    cursor.execute("UPDATE usuarios SET rendimento = ? WHERE cpf = ?", (rend_atual + float(valor_lucro), cpf))
    conn.commit()
    conn.close()

def processar_liberacao_aporte(cpf, valor_a_liberar):
    """Remove do saldo trancado e repassa para o rendimento livre."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET saldo = saldo - ?, rendimento = rendimento + ? WHERE cpf = ?", (float(valor_a_liberar), float(valor_a_liberar), cpf))
    conn.commit()
    conn.close()






