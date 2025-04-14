from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters,
    ContextTypes, CommandHandler, ChatMemberHandler
)
from deep_translator import GoogleTranslator
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")

# Tradução automática de mensagens (em grupos ou PV)
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
        "Se quiser me apoiar para que eu continue te ajudando, envie qualquer quantia de Solana para:\n\n"
        "`9XDRZZijaoEMmRmPj9a7i8CiNotwxGoV3gWzaakwFkgs`\n\n"
        "Obrigado pelo apoio! 🐸❤️",
        parse_mode="Markdown"
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        msg = (
            f"👥 Este grupo se chama: *{chat.title}*\n"
            f"🆔 ID do grupo: `{chat.id}`\n\n"
            "💬 Eu traduzo automaticamente mensagens entre inglês 🇺🇸 e português 🇧🇷.\n"
            "Basta me adicionar e começar a conversar!\n\n"
            "Use /donate para apoiar o projeto 🙏"
        )
    else:
        msg = (
            "👋 Olá! Eu sou o *YoloTranslate_bot*.\n\n"
            "💬 Traduza mensagens automaticamente entre inglês e português.\n"
            "Me adicione em um grupo ou use aqui no PV mesmo.\n\n"
            "Use /donate para apoiar meu desenvolvimento 🙏"
        )
    await update.message.reply_markdown(msg)

# Comando /yolotranslate
async def yolotranslate_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Sobre o YoloTranslate_bot:*\n\n"
        "Um bot simples, gratuito e direto ao ponto.\n"
        "Traduz automaticamente mensagens entre inglês e português 🇺🇸↔️🇧🇷.\n\n"
        "📌 Feito por amor à comunidade cripto e web3.\n"
        "💸 Se quiser me apoiar: /donate",
        parse_mode="Markdown"
    )

# Mensagem automática ao entrar em grupos
async def welcome_group(update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member and update.my_chat_member.new_chat_member.user.id == context.bot.id:
        chat = update.effective_chat
        await context.bot.send_message(
            chat_id=chat.id,
            text=(
                f"👋 Fui adicionado ao grupo *{chat.title}*!\n\n"
                "💬 Estou pronto para traduzir mensagens entre inglês 🇺🇸 e português 🇧🇷.\n"
                "Use /help para saber mais!"
            ),
            parse_mode="Markdown"
        )

# Inicialização
app = ApplicationBuilder().token(TOKEN).build()

# Comandos
app.add_handler(CommandHandler("donate", donate))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("yolotranslate", yolotranslate_info))

# Entrada em grupo
app.add_handler(ChatMemberHandler(welcome_group, ChatMemberHandler.MY_CHAT_MEMBER))

# Tradução automática
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

print("✅ YoloTranslate_bot online com comandos atualizados!")
app.run_polling()
