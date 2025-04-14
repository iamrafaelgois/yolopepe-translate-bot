from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, ContextTypes,
    CommandHandler, ChatMemberHandler
)
from deep_translator import GoogleTranslator
import requests
import os

# Token via variável de ambiente
TOKEN = os.getenv("BOT_TOKEN")

# Tradução automática (entre inglês e português)
async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and not text.startswith("/"):
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text)
            if translated == text:
                translated = GoogleTranslator(source='auto', target='pt').translate(text)
            await update.message.reply_text(f"🌐 {translated}")
        except:
            await update.message.reply_text("❌ Erro ao traduzir.")

# Comando /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://yolopepe-ping.onrender.com/status").json()
        await update.message.reply_text(f"✅ {res['project']} está {res['status']}")
    except:
        await update.message.reply_text("⚠️ Não foi possível verificar o status.")

# Comando /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://yolopepe-ping.onrender.com/info").json()
        msg = f"💡 *{res['name']}*\n🚀 {res['purpose']}\n📍 Chain: {res['chain']}\n👑 Criador: {res['creator']}"
        await update.message.reply_markdown(msg)
    except:
        await update.message.reply_text("⚠️ Não foi possível obter as informações.")

# Comando /donate
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 *Apoie o YoloTranslate_bot!*\n"
        "`9XDRZZijaoEMmRmPj9a7i8CiNotwxGoV3gWzaakwFkgs`\n"
        "Qualquer valor em SOL ou memecoins é bem-vindo 🙏🐸",
        parse_mode="Markdown"
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📜 *Comandos disponíveis:*\n\n"
        "/donate – Apoie o projeto com uma doação\n"
        "/status – Verifica o status do projeto\n"
        "/info – Informações sobre o $YOLOPEPE\n"
        "/help – Exibe esta mensagem\n\n"
        "💬 Também posso traduzir mensagens automaticamente entre inglês e português!"
    )
    await update.message.reply_markdown(help_text)

# Mensagem automática ao entrar em um grupo
async def welcome_group(update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member and update.chat_member.new_chat_member and update.chat_member.new_chat_member.user.id == context.bot.id:
        chat_id = update.chat_member.chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text="📨 Olá! Sou o *YoloTranslate_bot*.\n\n"
                 "Traduza mensagens automaticamente entre inglês e português 🇺🇸↔️🇧🇷\n"
                 "Quer apoiar o projeto?\nUse /donate\n\n"
                 "🛠 Feito por Rafael Gois",
            parse_mode="Markdown"
        )

# Inicialização do bot
app = ApplicationBuilder().token(TOKEN).build()

# Comandos
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("donate", donate))
app.add_handler(CommandHandler("help", help_command))

# Tradução automática
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

# Mensagem ao ser adicionado em grupo
app.add_handler(ChatMemberHandler(welcome_group, ChatMemberHandler.MY_CHAT_MEMBER))

print("✅ YoloTranslate_bot online com mensagem automática!")
app.run_polling()
