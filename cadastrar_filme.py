import sqlite3

def cadastrar_filme():
    conn = sqlite3.connect("filmes_series.db")
    cursor = conn.cursor()

    try:
        print("\n📥 Cadastro de Filme/Série")
        print("-" * 30)

        titulo = input("🎬 Título do Filme/Série: ").strip()
        sinopse = input("📚 Sinopse (pode ser link do Telegraph): ").strip()
        trailer = input("▶️ Link do Trailer (YouTube ou deixe vazio): ").strip()
        link = input("🎥 Link para Assistir (Telegram): ").strip()
        tipo = input("📺 Tipo (movie ou tv): ").strip().lower()

        if not titulo or not link or tipo not in ['movie', 'tv']:
            print("❌ Dados inválidos. Verifique o título, link e tipo.")
            return

        temporadas = ""
        if tipo == "tv":
            temporadas = input("📅 Temporadas disponíveis (ex: 1ª Temp, 2ª Temp, 3ª Temp): ").strip()

        cursor.execute('''
            INSERT INTO filmes_series (titulo, sinopse, trailer, link, tipo, temporadas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (titulo, sinopse, trailer, link, tipo, temporadas))

        conn.commit()
        print("✅ Cadastro realizado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao cadastrar: {e}")
    
    finally:
        conn.close()

# Executa
cadastrar_filme()
