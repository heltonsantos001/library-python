# create_db.py
# Criação do banco de dados SQLite para o sistema da biblioteca

import sqlite3

# Cria (ou conecta) ao banco biblioteca.db
conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

# Cria tabela livros dentro do banco
cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano_publicacao INTEGER NOT NULL,
    disponivel BOOLEAN NOT NULL
);
""")

# Salva e fecha
conn.commit()
conn.close()

print("Banco de dados 'biblioteca.db' criado com sucesso!")
