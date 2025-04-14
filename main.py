from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from deep_translator import GoogleTranslator
import os

# Token do bot via variável de ambiente
TOKEN = os.getenv("BOT_TOKEN")

# Tradução automática de mensagens (texto comum)
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
        "`9XDRZZijaoEMmRmPj9a7i8CiNotwxGoV3gWzaakwFkgs`\n"
        "Qualquer valor em SOL ou memecoins é bem-vindo 🙏🐸",
        parse_mode="Markdown"
    )

# Inicialização
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("donate", donate))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

print("✅ YoloTranslate_bot online e traduzindo!")
app.run_polling()
