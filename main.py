from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ChatMemberHandler
)
from deep_translator import GoogleTranslator
import requests
import os

# Token seguro via variável de ambiente
TOKEN = os.getenv("BOT_TOKEN")

# Tradução automática de mensagens (texto normal)
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

# Comando /donate
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 *Apoie o YoloTranslate_bot!*\n"
        "`9XDRZZijaoEMmRmPj9a7i8CiNotwxGoV3gWzaakwFkgs`\n\n"
        "Qualquer valor em SOL ou memecoins é bem-vindo 🙏🐸",
        parse_mode="Markdown"
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    chat_name = chat.title if chat.type in ["group", "supergroup"] else "este chat"

    help_text = (
        f"📜 *Comandos disponíveis em {chat_name}:*\n\n"
        "/help – Exibe esta mensagem\n"
        "/donate – Apoie este bot tradutor 🙏\n\n"
        "💬 Este bot traduz automaticamente mensagens entre inglês e português.\n"
        "Adicione em seu grupo e fale normalmente!\n\n"
        "🌍 Tradução bidirecional PT ↔️ EN"
    )
    await update.message.reply_markdown(help_text)

# Mensagem automática ao entrar em grupos
async def welcome_group(update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member.new_chat_member and update.chat_member.new_chat_member.user.id == context.bot.id:
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=(
                "👋 Olá! Sou o *YoloTranslate_bot*.\n\n"
                "Traduzo automaticamente mensagens entre inglês 🇺🇸 e português 🇧🇷.\n"
                "Use /help para ver os comandos.\n"
                "Use /donate para apoiar o projeto 🙏🐸"
            ),
            parse_mode="Markdown"
        )

# Inicialização do bot
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("donate", donate))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(ChatMemberHandler(welcome_group, ChatMemberHandler.MY_CHAT_MEMBER))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

print("✅ YoloTranslate_bot online e traduzindo em grupos!")
app.run_polling()
