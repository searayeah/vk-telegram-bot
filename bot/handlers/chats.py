from bot import (
    application,
    TG_CHAT_ID,
    CALLBACK_ANSWER,
    state,
    CHATS_NEXT,
    CHATS_PREV,
    CALLBACK_CHATS,
)
from telegram.ext import CommandHandler, filters
from vkbottle_types.objects import MessagesConversationPeerType
from bot.processors import vk
from bot.misc.keyboards import set_keyboard_8


async def chats(update, context):
    # button text max length 32
    current_page = 0

    next = [CHATS_NEXT, f"{CALLBACK_CHATS}.{current_page+1}"]
    prev = [CHATS_PREV, f"{CALLBACK_CHATS}.{current_page-1}"]
    unread_count, chats = await vk.get_chats(6, 0)
    args = [[value, f"{CALLBACK_ANSWER}{key}"] for key, value in chats.items()]
    reply_markup = set_keyboard_8(*args, prev, next)

    await update.message.reply_text(
        text=f"Unread: {unread_count}",
        reply_markup=reply_markup,
        parse_mode=state.parse_mode,
    )
    state.trailing = False


application.add_handler(
    CommandHandler("chats", chats, filters=filters.User(TG_CHAT_ID))
)
