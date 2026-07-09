import sqlite3

conn = sqlite3.connect("sistema_financeiro.db")
cursor = conn.cursor()

# Substitua 'usuarios' pelo nome real da sua tabela de clientes/testes
cursor.execute("SELECT * FROM usuarios;")
dados = cursor.fetchall()

for linha in dados:
    print(linha)

conn.close()
