import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from telegram.constants import ParseMode
from dotenv import load_dotenv
from sup_func import escape_markdown

load_dotenv()

# логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# состояния
MAINMENU, KNB, TALK = range(3)  # 0 1 2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update — информация о том, что произошло
    # update.effective_message - полная информация о сообщении
    # update.effective_user - полная информация о пользователе
    # update.effective_chat - полная информация о диалоге
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=escape_markdown(f"Привет, *{update.effective_user.first_name}*\n\n*Выберите игру:*\n/knb - камень-ножницы-бумага\n/talk - разговор"),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    return MAINMENU

async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы попали в игру разговор. Как дела?",
    )
    return TALK

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m_text = update.effective_message.text
    if m_text.lower() == "привет":
        m_text = "Привет"
    elif m_text.lower() == "как дела?":
        m_text = "Хорошо, а у тебя"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=m_text,
    )

async def rock_paper_scissors_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['a'] = 5
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы попали в игру камень-ножницы-бумага. Выберите один из вариантов: камень, ножницы, бумага.",
    )
    return KNB

async def rock_paper_scissors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"КНБ\n{context.user_data['a']}",
    )

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    # Handler - обработчик
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [CommandHandler("knb", rock_paper_scissors_start), CommandHandler("talk", talk_start)],
            KNB: [MessageHandler(filters.Regex("^(камень|ножницы|бумага)$"), rock_paper_scissors)]
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    # application.add_handler(
    #     MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    # )

    application.run_polling()
