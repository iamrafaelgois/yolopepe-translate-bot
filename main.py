from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters,
    ContextTypes, CommandHandler, ChatMemberHandler
)
from deep_translator import GoogleTranslator
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")

# Tradução automática
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
        f"💬 *Informações do Grupo:*\n"
        f"🏷 Nome: {chat.title or 'Privado'}\n"
        f"🆔 ID: `{chat.id}`\n"
        f"👥 Tipo: {chat.type}"
    )
    await update.message.reply_markdown(msg)

# Comando /donate
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 *Se quiser me apoiar para que eu continue te ajudando, envie qualquer quantia para:*\n"
        "`9XDRZZijaoEMmRmPj9a7i8CiNotwxGoV3gWzaakwFkgs`\n\n"
        "🐸 Obrigado por manter o YoloTranslate vivo!",
        parse_mode="Markdown"
    )

# Comando /yolotranslate
async def yolotranslate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 *O que é o YoloTranslate_bot?*\n\n"
        "É um bot de tradução automática para grupos e mensagens privadas.\n"
        "Traduz entre inglês 🇺🇸 e português 🇧🇷 automaticamente.\n"
        "Simples, útil e gratuito — criado com dedicação por Rafael Góis.",
        parse_mode="Markdown"
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📜 *Comandos disponíveis:*\n\n"
        "/donate – Apoie o YoloTranslate_bot\n"
        "/status – Status do projeto\n"
        "/info – Informações sobre o grupo\n"
        "/help – Exibe esta lista\n"
        "/yolotranslate – O que é e como funciona o YoloTranslate_bot\n\n"
        "💬 Traduza mensagens automaticamente entre 🇺🇸 e 🇧🇷 apenas enviando o texto!\n"
        "Simples, útil e gratuito — criado com dedicação por Rafael Góis."
    )
    await update.message.reply_markdown(help_text)

# Mensagem automática ao entrar em grupo
async def welcome_group(update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.chat_member.new_chat_member.user.id == context.bot.id:
            await context.bot.send_message(
                chat_id=update.chat.id,
                text=(
                    "👋 Olá! Sou o *YoloTranslate_bot*.\n\n"
                    "Traduza mensagens automaticamente entre 🇺🇸 e 🇧🇷!\n"
                    "Use /help para ver os comandos disponíveis.\n\n"
                    "Simples, útil e gratuito — criado com dedicação por Rafael Góis."
                ),
                parse_mode="Markdown"
            )
    except Exception as e:
        print("Erro ao enviar mensagem automática:", e)

# Inicialização
app = ApplicationBuilder().token(TOKEN).build()

# Comandos
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("donate", donate))
app.add_handler(CommandHandler("yolotranslate", yolotranslate))
app.add_handler(CommandHandler("help", help_command))

# Mensagem automática ao ser adicionado
app.add_handler(ChatMemberHandler(welcome_group, ChatMemberHandler.MY_CHAT_MEMBER))

# Tradução automática
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

print("✅ YoloTranslate_bot online com mensagem automática!")
app.run_polling()
