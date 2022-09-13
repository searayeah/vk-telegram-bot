import asyncio
from email.mime import application
import telegram
from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from vk_api.longpoll import Event, VkEventType
from vk_api.utils import get_random_id
from vkbottle import API, UserPolling
from vkbottle.user import User
from vkbottle_types.objects import MessagesConversationPeerType
from keyboards import set_keyboard_1, set_keyboard_8
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


POLLING = UserPolling(api=API(VK_TOKEN))

CHAT_STATE = {
    "type": None,
    "id": None,
    "name": None,
}
TRAILING_STATE = {
    "active": False,  # after my message False
    "name": None,
    "message_id": None,
    "sender_id": None,
    "text": None,
}
PINNED_MSG_ID = None


async def process_user(bot, event):
    response = {"chat_id": TG_CHAT_ID}
    logger.info(f"From user {event.user_id}")
    trailing_state = (
        TRAILING_STATE["active"] and TRAILING_STATE["sender_id"] == event.user_id
    )
    if trailing_state:
        logger.info(f"Trailing active")
        response[
            "text"
        ] = f"{TRAILING_STATE['name']}: {TRAILING_STATE['text']}\n{event.text}"
        response["message_id"] = TRAILING_STATE["message_id"]
        TRAILING_STATE["text"] = f"{TRAILING_STATE['text']}\n{event.text}"
    else:
        logger.info(f"Trailing inactive")
        user_info = await POLLING.api.users.get(event.user_id)

        TRAILING_STATE["name"] = f"*{user_info[0].first_name} {user_info[0].last_name}*"
        TRAILING_STATE["sender_id"] = event.user_id
        TRAILING_STATE["text"] = event.text
        response["text"] = f"{TRAILING_STATE['name']}: {event.text}"

    if CHAT_STATE["id"] != event.user_id:
        logger.info(f"Keyboard set")
        callback_data = f"user.{event.user_id}.{TRAILING_STATE['name']}"
        response["reply_markup"] = set_keyboard_1("Answer", callback_data)

    if trailing_state:
        logger.info(f"Message edit")
        await bot.edit_message_text(**response, parse_mode="MarkdownV2")
    else:
        logger.info(f"Message sent")
        message = await bot.send_message(**response, parse_mode="MarkdownV2")
        TRAILING_STATE["message_id"] = message.message_id
        TRAILING_STATE["active"] = True
    logger.info(f"TRAILING {TRAILING_STATE}\nRESPONSE {response}")


async def process_group(bot, event):
    response = {"chat_id": TG_CHAT_ID}
    logger.info(f"From group {event.group_id}")
    trailing_state = (
        TRAILING_STATE["active"] and TRAILING_STATE["sender_id"] == event.group_id
    )
    if trailing_state:
        logger.info(f"Trailing active")
        response[
            "text"
        ] = f"{TRAILING_STATE['name']}: {TRAILING_STATE['text']}\n{event.text}"
        response["message_id"] = TRAILING_STATE["message_id"]
        TRAILING_STATE["text"] = f"{TRAILING_STATE['text']}\n{event.text}"
    else:
        logger.info(f"Trailing inactive")
        group_info = await POLLING.api.groups.get_by_id(event.group_id)

        TRAILING_STATE["name"] = f"*{group_info[0].name}*"
        TRAILING_STATE["sender_id"] = event.group_id
        TRAILING_STATE["text"] = event.text
        response["text"] = f"{TRAILING_STATE['name']}: {event.text}"

    if CHAT_STATE["id"] != event.group_id:
        logger.info(f"Keyboard set")
        callback_data = f"group.{event.group_id}.{TRAILING_STATE['name']}"
        response["reply_markup"] = set_keyboard_1("Answer", callback_data)

    if trailing_state:
        logger.info(f"Message edit")
        await bot.edit_message_text(**response, parse_mode="MarkdownV2")
    else:
        logger.info(f"Message sent")
        message = await bot.send_message(**response, parse_mode="MarkdownV2")
        TRAILING_STATE["message_id"] = message.message_id
        TRAILING_STATE["active"] = True
    logger.info(f"TRAILING {TRAILING_STATE}\nRESPONSE {response}")


async def process_chat(bot, event):
    response = {"chat_id": TG_CHAT_ID}
    logger.info(f"From chat {event.chat_id}")
    trailing_state = (
        TRAILING_STATE["active"] and TRAILING_STATE["sender_id"] == event.chat_id
    )

    user_info = await POLLING.api.users.get(event.user_id)

    if trailing_state:
        logger.info(f"Trailing active")

        response["text"] = (
            f"{TRAILING_STATE['name']}\n{TRAILING_STATE['text']}\n"
            + f"{user_info[0].first_name} {user_info[0].last_name}: {event.text}"
        )
        response["message_id"] = TRAILING_STATE["message_id"]
        TRAILING_STATE["text"] = (
            f"{TRAILING_STATE['text']}\n"
            + f"{user_info[0].first_name} {user_info[0].last_name}: {event.text}"
        )
    else:
        logger.info(f"Trailing inactive")
        chat_info = await POLLING.api.messages.get_conversations_by_id(
            2000000000 + event.chat_id
        )

        TRAILING_STATE["name"] = f"*{chat_info.items[0].chat_settings.title}*"
        TRAILING_STATE["sender_id"] = event.chat_id
        TRAILING_STATE[
            "text"
        ] = f"{user_info[0].first_name} {user_info[0].last_name}: {event.text}"
        response["text"] = (
            f"{TRAILING_STATE['name']}\n"
            + f"{user_info[0].first_name} {user_info[0].last_name}: {event.text}"
        )

    if CHAT_STATE["id"] != 2000000000 + event.chat_id:
        logger.info(f"Keyboard set")
        callback_data = f"chat.{2000000000 + event.chat_id}.{TRAILING_STATE['name']}"
        response["reply_markup"] = set_keyboard_1("Answer", callback_data)

    if trailing_state:
        logger.info(f"Message edit")
        await bot.edit_message_text(**response, parse_mode="MarkdownV2")
    else:
        logger.info(f"Message sent")
        message = await bot.send_message(**response, parse_mode="MarkdownV2")
        TRAILING_STATE["message_id"] = message.message_id
        TRAILING_STATE["active"] = True
    logger.info(f"TRAILING {TRAILING_STATE}\nRESPONSE {response}")


async def process_update(bot, event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # for testing purposes
        logger.info(f"Entered new message")
        if event.from_user:
            await process_user(bot, event)
        elif event.from_group:
            await process_group(bot, event)
        elif event.from_chat:
            await process_chat(bot, event)


async def run_polling(bot):
    async for event in POLLING.listen():
        for update in event.get("updates", []):
            event = Event(update)  # IMPORTANT change vkbottle longpoll version to 3
            # vk_api Event class works only with ver 3 longpoll
            # while vkbottle uses default version 0
            await process_update(bot, event)


async def answer_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split(".")
    CHAT_STATE["type"] = callback_data[0]
    CHAT_STATE["id"] = int(callback_data[1])
    CHAT_STATE["name"] = callback_data[2]

    output = f"Now talking with {CHAT_STATE['name']}"
    message = await query.message.reply_text(text=output)
    await message.pin()
    TRAILING_STATE["active"] = False


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CHAT_STATE["type"] != None:
        await POLLING.api.messages.send(
            peer_id=CHAT_STATE["id"]
            if CHAT_STATE["type"] in ("user", "chat")
            else -CHAT_STATE["id"],
            random_id=get_random_id(),
            message=update.message.text,
        )
    else:
        await update.message.reply_text(text="No chat selected")
    TRAILING_STATE["active"] = False


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = f"Now talking with {CHAT_STATE['name']}"
    await update.message.reply_text(text=output)
    TRAILING_STATE["active"] = False


async def chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ## need review
    chats = await POLLING.api.messages.get_conversations(count=10)
    outputs = []
    callbacks = []
    # print(chats)
    # print("test")

    async def process_chat(i):
        print(chats.items[i].conversation.peer.type)
        if chats.items[i].conversation.peer.type == MessagesConversationPeerType.CHAT:
            print("CHAT CHAT")
            output = f"Беседа {chats.items[i].conversation.chat_settings.title}"
            callback_object = (
                f"chat.{chats.items[i].conversation.peer.id}."
                + f"{chats.items[i].conversation.chat_settings.title}"
            )
            return output, callback_object
        elif chats.items[i].conversation.peer.type == MessagesConversationPeerType.USER:
            print("USER USER")
            user_info = await POLLING.api.users.get(chats.items[i].conversation.peer.id)
            output = f"{user_info[0].first_name} " + f"{user_info[0].last_name}"
            callback_object = (
                f"user.{chats.items[i].conversation.peer.id}."
                + f"{user_info[0].first_name} {user_info[0].last_name}"
            )
            return output, callback_object
        elif (
            chats.items[i].conversation.peer.type == MessagesConversationPeerType.GROUP
        ):
            group_info = await POLLING.api.groups.get_by_id(
                abs(chats.items[i].conversation.peer.id)
            )
            output = f"Сообщество {group_info[0].name}"
            callback_object = (
                f"group.{abs(chats.items[i].conversation.peer.id)}.{group_info[0].name}"
            )
            return output, callback_object

    outputs = await asyncio.gather(*[process_chat(i) for i in range(8)])
    outputs = [item for sublist in outputs for item in sublist]

    reply_markup = set_keyboard_8(*(outputs[::2] + outputs[1::2]))
    await update.message.reply_text(
        text=f"Непрочитанных: {chats.unread_count}",
        reply_markup=reply_markup,
    )
    # print(chats)
    TRAILING_STATE["active"] = False


async def main():

    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CommandHandler("now", now))
    application.add_handler(CommandHandler("chats", chats))

    application.add_handler(CallbackQueryHandler(answer_button))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, send_message)
    )

    async with application:

        await application.updater.start_polling()
        await application.start()

        await run_polling(bot=application.bot)

        # run until it receives a stop signal
        await application.updater.stop()
        await application.stop()


asyncio.run(main())
