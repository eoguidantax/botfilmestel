import os
import asyncio
import sqlite3
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

# Conectar ao banco
conn = sqlite3.connect('filmes_series.db')
cursor = conn.cursor()

# Garantir que a tabela existe
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

# Iniciar cliente Telethon
client = TelegramClient('listener_session', API_ID, API_HASH)

def identificar_tipo(texto):
    texto_lower = texto.lower()
    if "temporada" in texto_lower or "episódio" in texto_lower or "episodio" in texto_lower:
        return "série"
    return "filme"

def extrair_sinopse(mensagem):
    for parte in mensagem.split("\n"):
        if "telegraph" in parte:
            return parte.strip()
    return ""

def extrair_trailer(mensagem):
    for parte in mensagem.split("\n"):
        if "youtube.com" in parte or "youtu.be" in parte:
            return parte.strip()
    return ""

@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    mensagem = event.message.message.strip()

    # Extrair partes da mensagem
    partes = mensagem.split('\n')
    nome = partes[0]
    link = next((p for p in partes if 'http' in p and 'telegraph' not in p and 'youtu' not in p), None)
    sinopse = extrair_sinopse(mensagem)
    trailer = extrair_trailer(mensagem)
    tipo = identificar_tipo(mensagem)

    if nome and link:
        cursor.execute("SELECT * FROM filmes_series WHERE nome = ?", (nome,))
        existe = cursor.fetchone()
        if not existe:
            cursor.execute(
                "INSERT INTO filmes_series (nome, link, tipo, sinopse, trailer) VALUES (?, ?, ?, ?, ?)",
                (nome, link, tipo, sinopse, trailer)
            )
            conn.commit()
            print(f"[✔] Adicionado: {nome}")
        else:
            print(f"[!] Já existe: {nome}")

async def main():
    print("👂 Ouvindo o canal...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
