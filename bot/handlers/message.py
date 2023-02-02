from bot import application
from telegram.ext import MessageHandler, filters
from bot import state
from bot.processors import vk


async def message(update, context):
    # attachments and etc...
    if state.active_conversation_id:
        await vk.send_message(state.active_conversation_id, text)
    else:
        text = "No chat selected"
        await update.message.reply_text(text=text, parse_mode=state.parse_mode)
        state.trailing = False


application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
