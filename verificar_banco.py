import sqlite3

# Conecta ou cria o banco
conn = sqlite3.connect("filmes_series.db")
cursor = conn.cursor()

# Cria a tabela com validação básica
cursor.execute('''
    CREATE TABLE IF NOT EXISTS filmes_series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        sinopse TEXT,
        trailer TEXT,
        link TEXT NOT NULL,
        tipo TEXT DEFAULT "movie" CHECK(tipo IN ("movie", "tv")),
        temporadas TEXT
    )
''')

conn.commit()
conn.close()
print("✅ Banco de dados 'filmes_series.db' verificado/criado com a tabela 'filmes_series'.")
