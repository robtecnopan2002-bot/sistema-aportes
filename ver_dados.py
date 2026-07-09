import sqlite3

# Conecta ao arquivo do banco
conn = sqlite3.connect("sistema_financeiro.db")
cursor = conn.cursor()

# 1. Descobre o nome de todas as tabelas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("--- TABELAS ENCONTRADAS ---")
for tab in tabelas:
    nome_tabela = tab[0]
    print(f"\nDados da tabela: {nome_tabela}")
    print("-" * 30)
    
    # 2. Busca e mostra todos os dados da tabela atual
    try:
        cursor.execute(f"SELECT * FROM {nome_tabela};")
        linhas = cursor.fetchall()
        
        if not linhas:
            print("(Tabela vazia)")
        for linha in linhas:
            print(linha)
    except sqlite3.Error as e:
        print(f"Erro ao ler tabela: {e}")

conn.close()

