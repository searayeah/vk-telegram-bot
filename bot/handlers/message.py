from bot import application
from telegram.ext import MessageHandler, filters
from bot import state, TG_CHAT_ID
from bot.processors import vk


async def message(update, context):
    # attachments and etc...
    # formatting message for vk
    if state.active_conversation_id:
        await vk.send_message(state.active_conversation_id, update.message.text)
    else:
        text = "No chat selected"
        await update.message.reply_text(text=text, parse_mode=state.parse_mode)
    state.trailing = False

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(TG_CHAT_ID), message))
