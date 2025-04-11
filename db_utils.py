import sqlite3

def criar_tabela():
    conn = sqlite3.connect('filmes_series.db')
    cursor = conn.cursor()

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
    print("✅ Tabela 'filmes_series' criada ou já existente com as colunas corretas.")

# Executa ao rodar o script
if __name__ == "__main__":
    criar_tabela()
