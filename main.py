from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from deep_translator import GoogleTranslator
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")

# Tradução automática de mensagens
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
    chat = update.effective_chat
    msg = (
        f"ℹ️ *Informações do grupo:*\n\n"
        f"*Nome:* {chat.title}\n"
        f"*ID:* `{chat.id}`\n"
        f"*Tipo:* {chat.type}"
    )
    await update.message.reply_markdown(msg)

# Comando /donate
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 *Apoie o YoloTranslate_bot!*\n\n"
        "Se quiser me apoiar para que eu continue te ajudando, envie qualquer quantia de Solana para:\n"
        "`9XDRZZijaoEMmRmPj9a7i8CiNotwxGoV3gWzaakwFkgs`\n\n"
        "Obrigado de coração 🐸💚",
        parse_mode="Markdown"
    )

# Comando /yolotranslate
async def yolotranslate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *Sobre o YoloTranslate_bot:*\n\n"
        "Sou um bot criado para ajudar comunidades bilíngues a se comunicarem melhor, traduzindo mensagens automaticamente entre *inglês e português*. 🇺🇸↔️🇧🇷\n\n"
        "Simples, útil e gratuito — criado com amor pelo @rafaelgoissant0 💻🐸",
        parse_mode="Markdown"
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📜 *Comandos disponíveis:*\n\n"
        "/donate - Apoie o YoloTranslate_bot\n"
        "/status - Verifica o status do projeto\n"
        "/info - Informações sobre o grupo\n"
        "/help - Exibe a lista de comandos\n"
        "/yolotranslate - O que é e como funciona o YoloTranslate_bot\n\n"
        "💬 Também posso traduzir mensagens automaticamente entre inglês e português!"
    )
    await update.message.reply_markdown(help_text)

# Inicialização do bot
app = ApplicationBuilder().token(TOKEN).build()

# Handlers de comandos
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("donate", donate))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("yolotranslate", yolotranslate))

# Tradução automática
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

print("✅ YoloTranslate_bot online com mensagem automática!")
app.run_polling()
