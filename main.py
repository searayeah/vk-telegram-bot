import asyncio
import logging
import os
from itertools import compress

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
from messageprocessor import MessageProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

TG_CHAT_ID = os.environ["TG_CHAT_ID"]
VK_TOKEN = os.environ["VK_TOKEN"]
TG_TOKEN = os.environ["TG_TOKEN"]

POLLING = UserPolling(api=API(VK_TOKEN))

POLLING.api.messages.get_by_id


async def run_polling(context):
    async for event in POLLING.listen():
        for update in event.get("updates", []):
            event = Event(update)  # IMPORTANT change vkbottle longpoll version to 3
            # vk_api Event class works only with ver 3 longpoll
            # while vkbottle uses default version 0
            if (
                event.type == VkEventType.MESSAGE_NEW and event.to_me
            ):  # for testing purposes
                logger.info(f"Entered new message")
                await context["message_processor"].process(event)


async def answer_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split(".")

    context.bot_data["message_processor"].active_conversation_id = int(callback_data[0])
    context.bot_data["message_processor"].active_conversation_name = callback_data[1]

    output = f"Now talking with {context.bot_data['message_processor'].active_conversation_name}"
    message = await query.message.reply_text(
        text=output, parse_mode=context.bot_data["message_processor"].parse_mode
    )
    await message.pin()
    context.bot_data["message_processor"].trailing = False


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot_data["message_processor"].active_conversation_id != None:
        await POLLING.api.messages.send(
            peer_id=context.bot_data["message_processor"].active_conversation_id,
            random_id=get_random_id(),
            message=update.message.text,
        )
    else:
        await update.message.reply_text(text="No chat selected")
    context.bot_data["message_processor"].trailing = False


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TO-DO
    # if answer_name == none
    output = f"Now talking with {context.bot_data['message_processor'].active_conversation_name}"
    await update.message.reply_text(
        text=output, parse_mode=context.bot_data["message_processor"].parse_mode
    )
    context.bot_data["message_processor"].trailing = False


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

    application.bot_data["message_processor"] = MessageProcessor(
        application.bot, POLLING, TG_CHAT_ID
    )
    # application.bot_data["answer_type"] = None
    # application.bot_data["answer_id"] = None
    # application.bot_data["answer_name"] = None

    async with application:

        await application.updater.start_polling()
        await application.start()

        # await test()
        await run_polling(context=application.bot_data)

        # run until it receives a stop signal
        await application.updater.stop()
        await application.stop()


asyncio.run(main())
