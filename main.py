from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, ContextTypes,
    CommandHandler, ChatMemberHandler
)
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
    group_name = chat.title if chat.type in ["group", "supergroup"] else "essa conversa"
    await update.message.reply_text(f"ℹ️ Você está em {group_name}.")

# Comando /donate
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 *Se quiser me apoiar para que eu continue te ajudando, envie qualquer quantia de Solana para:*\n\n"
        "`9XDRZZijaoEMmRmPj9a7i8CiNotwxGoV3gWzaakwFkgs`\n\n"
        "🙏 Obrigado de coração! 🐸",
        parse_mode="Markdown"
    )

# Comando /yolotranslate
async def yolotranslate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐸 *YoloTranslate_bot* traduz automaticamente mensagens entre português e inglês em qualquer grupo.\n\n"
        "Simples, útil e gratuito — criado com amor por Rafael Góis ❤️",
        parse_mode="Markdown"
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    name = chat.title if chat.title else "este grupo"
    await update.message.reply_text(
        f"📋 *Comandos disponíveis em {name}:*\n\n"
        "/donate – Apoie o YoloTranslate_bot\n"
        "/status – Status do projeto\n"
        "/info – Nome do grupo atual\n"
        "/yolotranslate – O que é o YoloTranslate_bot\n"
        "/help – Esta mensagem de ajuda",
        parse_mode="Markdown"
    )

# Mensagem ao entrar em grupo
async def welcome_group(update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member and update.chat_member.new_chat_member.user.id == context.bot.id:
        chat_id = update.chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "👋 Olá! Sou o *YoloTranslate_bot*.\n"
                "Traduza mensagens automaticamente entre inglês e português 🇺🇸↔️🇧🇷\n"
                "Use /help para ver os comandos disponíveis.\n\n"
                "Simples, útil e gratuito — criado com amor por Rafael Góis ❤️"
            ),
            parse_mode="Markdown"
        )

# Inicialização
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("donate", donate))
app.add_handler(CommandHandler("yolotranslate", yolotranslate))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(ChatMemberHandler(welcome_group, ChatMemberHandler.MY_CHAT_MEMBER))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

print("✅ YoloTranslate_bot online com mensagem automática!")
app.run_polling()
