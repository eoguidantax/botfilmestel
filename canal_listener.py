import os
import sqlite3
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Carrega variáveis de ambiente
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "listener"
CHANNEL_USERNAME = "@acessolivr3"  # canal de origem
DB_PATH = "filmes_series.db"

# Inicializa o cliente
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Função para inserir no banco
def inserir_filme(nome, link, tipo='Filme', sinopse=None, trailer=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO filmes_series (nome, link, tipo, sinopse, trailer)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, link, tipo, sinopse, trailer))
    conn.commit()
    conn.close()
    print(f"✅ Inserido no banco: {nome}")

# Escuta novas mensagens do canal
@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    msg = event.message.message

    if "http" in msg:
        partes = msg.split("\n")
        nome = partes[0].strip()
        link = next((p for p in partes if "http" in p), None)
        if nome and link:
            inserir_filme(nome, link)

client.start()
print("👂 Ouvindo mensagens do canal @acessolivr3...")
client.run_until_disconnected()
