import os
import requests
import sqlite3
from telebot import TeleBot, types
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Inicializa o bot
bot = TeleBot(TELEGRAM_TOKEN)

# Remove webhook para evitar conflito com polling
def deletar_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ Webhook removido com sucesso!")
    else:
        print("❌ Erro ao remover webhook:", response.text)

deletar_webhook()

# /start com botões interativos
@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🎬 Filmes")
    btn2 = types.KeyboardButton("📺 Séries")
    markup.add(btn1, btn2)

    texto = (
        "👋 Hey, parça! Bem-vindo ao *Claquete!*\n\n"
        "🎥 Me diga o nome de um filme ou série que você está procurando,\n"
        "ou clique em um dos botões abaixo para ver o que temos disponível!"
    )
    bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode='Markdown')

# Admin: /listar tudo do banco
@bot.message_handler(commands=['listar'])
def listar_como_admin(message):
    try:
        conn = sqlite3.connect("filmes_series.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, link FROM filmes_series WHERE tipo = 'Filme'")
        filmes = cursor.fetchall()
        conn.close()

        if filmes:
            resposta = "📋 *Filmes cadastrados:*\n\n"
            for nome, link in filmes:
                resposta += f"🎬 {nome}\n🔗 {link}\n\n"
            bot.send_message(message.chat.id, resposta, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "⚠️ Nenhum filme encontrado.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao acessar o banco:\n{e}")

# Comando para clientes - /filmes
@bot.message_handler(commands=['filmes'])
def listar_filmes(message):
    enviar_lista_filmes(message.chat.id)

# Comando para clientes - /series
@bot.message_handler(commands=['series'])
def listar_series(message):
    enviar_lista_series(message.chat.id)

# Atalhos pelos botões de texto
@bot.message_handler(func=lambda message: message.text == "🎬 Filmes")
def filmes_botao(message):
    enviar_lista_filmes(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "📺 Séries")
def series_botao(message):
    enviar_lista_series(message.chat.id)

# Funções auxiliares para listar conteúdo
def enviar_lista_filmes(chat_id):
    try:
        conn = sqlite3.connect("filmes_series.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, link FROM filmes_series WHERE tipo = 'Filme' ORDER BY nome ASC")
        filmes = cursor.fetchall()
        conn.close()

        if filmes:
            resposta = "🎬 *Catálogo de Filmes:*\n\n"
            for nome, link in filmes:
                resposta += f"🎞️ *{nome}*\n👉 [Assistir agora]({link})\n\n"
            bot.send_message(chat_id, resposta, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "📭 Nenhum filme disponível no momento.")
    except Exception as e:
        bot.send_message(chat_id, f"Erro ao carregar filmes:\n{e}")

def enviar_lista_series(chat_id):
    try:
        conn = sqlite3.connect("filmes_series.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, link FROM filmes_series WHERE tipo = 'Série' ORDER BY nome ASC")
        series = cursor.fetchall()
        conn.close()

        if series:
            resposta = "📺 *Catálogo de Séries:*\n\n"
            for nome, link in series:
                resposta += f"📘 *{nome}*\n👉 [Assistir agora]({link})\n\n"
            bot.send_message(chat_id, resposta, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "📭 Nenhuma série disponível no momento.")
    except Exception as e:
        bot.send_message(chat_id, f"Erro ao carregar séries:\n{e}")

# 🧠 Busca por nome com todos os dados
@bot.message_handler(func=lambda message: True)
def buscar_por_nome(message):
    termo = message.text.strip().lower()

    if termo in ["🎬 filmes", "📺 séries"]:
        return

    try:
        conn = sqlite3.connect("filmes_series.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, sinopse, link, tipo, trailer FROM filmes_series")
        resultados = cursor.fetchall()
        conn.close()

        encontrados = []
        for nome, sinopse, link, tipo, trailer in resultados:
            if termo in nome.lower():
                encontrados.append((nome, sinopse, link, tipo, trailer))

        if encontrados:
            resposta = f"🍿 Opa! Tá aqui, chefe! Tudo que eu tenho de *'{message.text}'*:\n\n"
            for nome, sinopse, link, tipo, trailer in encontrados:
                emoji = "🎬" if tipo == "Filme" else "📺"
                resposta += (
                    f"{emoji} *{nome}*\n"
                    f"📝 _{sinopse}_\n"
                    f"🎭 Tipo: {tipo}\n"
                    f"👉 [🎥 Assistir agora]({link})\n"
                )
                if trailer:
                    resposta += f"▶️ [Veja o trailer]({trailer})\n"
                resposta += "\n"
            bot.send_message(message.chat.id, resposta, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "😕 Não achei nada com esse nome...\nTenta outro ou usa os botões abaixo 👇")
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao buscar:\n{e}")

# Início do bot
print("🎬 Bot rodando com sucesso!")
bot.polling()
