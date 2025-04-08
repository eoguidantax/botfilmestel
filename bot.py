import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Carrega variáveis do .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Caminho do banco
db_path = "filmes_series.db"
print("Caminho do banco de dados:", os.path.abspath(db_path))

# Garante que a tabela exista
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS filmes_series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        link TEXT,
        tipo TEXT,
        sinopse TEXT,
        trailer TEXT
    )
""")
conn.commit()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 E aí, parça! Pronto pra ação?\n\n🔎 É só me mandar o nome do filme ou série que eu te mostro tudo na hora!\n\n🍿 Bora lá!"
    )

# /listar
async def listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, tipo, link FROM filmes_series ORDER BY nome")
    filmes = cursor.fetchall()

    if not filmes:
        await update.message.reply_text("❌ Nenhum filme cadastrado ainda.")
        return

    resposta = "📽️ *Filmes/Séries Cadastrados:*\n\n"
    for nome, tipo, link in filmes:
        resposta += f"🎬 *{nome}* — _{tipo}_\n▶️ [Assistir agora]({link})\n\n"

    await update.message.reply_markdown(resposta)

# Buscar filme por nome
async def buscar_filme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    busca = update.message.text.strip().lower()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, tipo, sinopse, trailer, link FROM filmes_series WHERE LOWER(nome) LIKE ?", (f"%{busca}%",))
    resultados = cursor.fetchall()

    if not resultados:
        await update.message.reply_text("❌ Não encontrei nada com esse nome. Tenta outro aí, parça!")
        return

    for nome, tipo, sinopse, trailer, link in resultados:
        texto = f"🎬 *{nome}*\n📺 Tipo: _{tipo}_\n\n📖 [Sinopse]({sinopse})\n🎞️ [Trailer]({trailer})"
        botao = [[InlineKeyboardButton("▶️ Assistir agora", url=link)]]
        markup = InlineKeyboardMarkup(botao)
        await update.message.reply_markdown(texto, reply_markup=markup)

# Inicia o bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("listar", listar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_filme))
    print("🤖 Bot está rodando...")
    app.run_polling()
