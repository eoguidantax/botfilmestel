import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('filmes_series.db')
cursor = conn.cursor()

# Cria a tabela com os campos corretos
cursor.execute('''
CREATE TABLE IF NOT EXISTS filmes_series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    link TEXT NOT NULL,
    tipo TEXT,
    sinopse TEXT,
    trailer TEXT
)
''')

conn.commit()
conn.close()

print("Tabela 'filmes_series' criada ou já existente com as colunas corretas.")
