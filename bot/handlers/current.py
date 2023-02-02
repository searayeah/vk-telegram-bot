from bot import application
from telegram.ext import CommandHandler


async def now(update, context):
    # TO-DO
    # if answer_name == none
    # await update.message.reply_text(**context.bot_data["message_processor"].now())

    await update.message.reply_text("now")


application.add_handler(CommandHandler("now", now))
