from bot import application, state
from telegram.ext import CommandHandler, filters
from bot import TG_CHAT_ID


async def current(update, context):
    if state.active_conversation_name:
        text = f"Now talking with {state.active_conversation_name}"
    else:
        text = f"No chat selected"
        await update.message.reply_text(text=text, parse_mode=state.parse_mode)
    state.trailing = False


application.add_handler(CommandHandler("current", current, filters=filters.User(int(TG_CHAT_ID))))
