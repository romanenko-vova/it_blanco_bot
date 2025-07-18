import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv

load_dotenv()

# логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update — информация о том, что произошло
    # update.effective_message - полная информация о сообщении
    # update.effective_user - полная информация о пользователе
    # update.effective_chat - полная информация о диалоге
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет, {update.effective_user.first_name}",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m_text = update.effective_message.text
    if m_text.lower() == 'привет':
        m_text = 'Привет'
    elif m_text.lower() == 'как дела?':
        m_text = 'Хорошо, а у тебя'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=m_text,
    )
    
async def tic_tac_toe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="КНБ",
    )

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    # Handler - обработчик
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.Regex('^(камень|ножницы|бумага)$'), tic_tac_toe)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()
