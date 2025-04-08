import sqlite3

def init_db():
    conn = sqlite3.connect("filmes_series.db")
    cursor = conn.cursor()

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
    print("✅ Banco de dados verificado/criado com sucesso!")
