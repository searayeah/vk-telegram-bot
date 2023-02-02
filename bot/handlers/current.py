from bot import application, state
from telegram.ext import CommandHandler


async def current(update, context):
    # TO-DO
    # if answer_name == none
    text = f"Now talking with {state.active_conversation_name}"
    await update.message.reply_text(text=text, parse_mode=state.parse_mode)
    state.trailing = False


application.add_handler(CommandHandler("current", current))
