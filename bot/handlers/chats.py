from bot import (
    application,
    TG_CHAT_ID,
    CALLBACK_ANSWER,
    state,
    CHATS_NEXT,
    CHATS_PREV,
    CALLBACK_CHATS,
    CHATS_PAGE,
    CHATS_UNREAD,
)
from telegram.ext import CommandHandler, CallbackQueryHandler, filters
from bot.processors import vk
from bot.misc.keyboards import (
    set_keyboard_rows_2,
    set_keyboard_3,
    set_keyboard_4,
    set_keyboard_5,
    set_keyboard_6,
    set_keyboard_7,
    set_keyboard_8,
)

buttons = list(range(2, 9))
keyboards = [
    set_keyboard_rows_2,
    set_keyboard_3,
    set_keyboard_4,
    set_keyboard_5,
    set_keyboard_6,
    set_keyboard_7,
    set_keyboard_8,
]
keyboards_dispatcher = dict(zip(buttons, keyboards))


async def set_buttons(page):
    button_count = 6
    chats_count, unread_count, chats = await vk.get_chats(
        button_count, button_count * page
    )
    max_page = chats_count // button_count  # actual page count -1

    args = [[value, f"{CALLBACK_ANSWER}.{key}"] for key, value in chats.items()]
    if page != 0:
        prev = [CHATS_PREV, f"{CALLBACK_CHATS}.{page-1}"]
        args.append(prev)
    if page != max_page:
        next = [CHATS_NEXT, f"{CALLBACK_CHATS}.{page+1}"]
        args.append(next)
    reply_markup = keyboards_dispatcher[len(args)](*args)

    return max_page, unread_count, reply_markup


async def turn_page(update, context):
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split(".")

    max_page, unread_count, reply_markup = await set_buttons(int(callback_data[1]))
    await query.edit_message_text(
        text=f"*{CHATS_PAGE} {callback_data[1]}/{max_page}*\n_{CHATS_UNREAD}: {unread_count}_",
        reply_markup=reply_markup,
        parse_mode=state.parse_mode,
    )


async def chats(update, context):
    page = 0  # pages start with 0
    max_page, unread_count, reply_markup = await set_buttons(page)
    await update.message.reply_text(
        text=f"*{CHATS_PAGE} {page}/{max_page}*\n_{CHATS_UNREAD}: {unread_count}_",
        reply_markup=reply_markup,
        parse_mode=state.parse_mode,
    )
    state.trailing = False


application.add_handler(
    CommandHandler("chats", chats, filters=filters.User(TG_CHAT_ID))
)
application.add_handler(CallbackQueryHandler(turn_page, CALLBACK_CHATS))
