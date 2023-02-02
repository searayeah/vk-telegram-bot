import asyncio

# import logging
# import os
# from itertools import compress

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
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from os import environ
from vk_api.longpoll import Event, VkEventType
from vk_api.utils import get_random_id
from vkbottle import API, UserPolling
from vkbottle.user import User
from vkbottle_types.objects import MessagesConversationPeerType
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import asyncio

# from vk_api.longpoll import Event, VkEventType
# from vk_api.utils import get_random_id
# from vkbottle import API, UserPolling
# from vkbottle.user import User
# from vkbottle_types.objects import MessagesConversationPeerType

# from .processors import MessageProcessor
from bot import application, polling
# from .processors.vk import run_polling
from .processors.messageprocessor import message_processor
# from .handlers import button, chats, current, echo, message
from .handlers import echo
# application.bot_data["processor"] = MessageProcessor(
#     application.bot, polling, EnvVars.TG_CHAT_ID
# )
# await run_polling(application.bot_data["processor"])

async def vk_polling():
    async for event in polling.listen():
        for update in event.get("updates", []):
            event = Event(update)  # IMPORTANT change vkbottle longpoll version to 3
            # vk_api Event class works only with ver 3 longpoll
            # while vkbottle uses default version 0
            if (
                event.type == VkEventType.MESSAGE_NEW  # and event.to_me
            ):  # for testing purposes
                # logger.info(f"Entered new message")
                await message_processor.process(event)



async def main():
    async with application:
        await application.start()
        await application.updater.start_polling()

        await vk_polling()

        await application.updater.stop()
        await application.stop()


asyncio.run(main())
