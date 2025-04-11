import sqlite3

def cadastrar_filme():
    conn = sqlite3.connect("filmes_series.db")
    cursor = conn.cursor()

    try:
        print("\n📥 Cadastro de Filme ou Série")
        print("-" * 30)

        nome = input("🎬 Nome do Filme/Série: ").strip()
        sinopse = input("📚 Sinopse (link do Telegraph ou deixe em branco): ").strip()
        trailer = input("▶️ Link do Trailer (YouTube ou deixe em branco): ").strip()
        link = input("🎥 Link para Assistir (Telegram): ").strip()
        tipo = input("📺 Tipo (filme ou série): ").strip().lower()

        if not nome or not link or tipo not in ['filme', 'série']:
            print("❌ Dados inválidos. Verifique o nome, link e tipo (filme/série).")
            return

        cursor.execute('''
            INSERT INTO filmes_series (nome, sinopse, trailer, link, tipo)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, sinopse, trailer, link, tipo))

        conn.commit()
        print(f"✅ '{nome}' cadastrado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao cadastrar: {e}")
    
    finally:
        conn.close()

# Executa
cadastrar_filme()
