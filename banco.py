import sqlite3

DB_NAME = "sistema_financeiro.db"

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
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nome, cpf, telefone, cep, email, senha, saldo, status, plano_ativo, rendimento FROM usuarios WHERE cpf = ?", (cpf,))
        linha = cursor.fetchone()
    except sqlite3.OperationalError:
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN rendimento REAL DEFAULT 0.0;")
            conn.commit()
        except Exception:
            pass
        cursor.execute("SELECT nome, cpf, telefone, cep, email, senha, saldo, status, plano_ativo, rendimento FROM usuarios WHERE cpf = ?", (cpf,))
        linha = cursor.fetchone()
    conn.close()
    if linha:
        return {
            "nome": linha[0],
            "cpf": linha[1],
            "telefone": linha[2],
            "cep": linha[3],
            "email": linha[4],
            "senha": linha[5],
            "saldo": linha[6],
            "status": linha[7],
            "plano_ativo": linha[8],
            "rendimento": linha[9] if len(linha) > 9 and linha[9] is not None else 0.0
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

def atualizar_rendimento(cpf, novo_valor_rendimento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET rendimento = ? WHERE cpf = ?", (novo_valor_rendimento, cpf))
    conn.commit()
    conn.close()

def atualizar_saldos_liberacao(cpf, valor_a_liberar):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET saldo = saldo - ?, rendimento = rendimento + ? WHERE cpf = ?", (valor_a_liberar, valor_a_liberar, cpf))
    conn.commit()
    conn.close()





