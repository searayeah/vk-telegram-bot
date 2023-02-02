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
from dotenv import load_dotenv
from vk_api.longpoll import Event, VkEventType
from vk_api.utils import get_random_id
from vkbottle import API, UserPolling
from vkbottle.user import User
from vkbottle_types.objects import MessagesConversationPeerType
from os import environ
load_dotenv()

TG_CHAT_ID = environ["TG_CHAT_ID"]
VK_TOKEN = environ["VK_TOKEN"]
TG_TOKEN = environ["TG_TOKEN"]

application = Application.builder().token(TG_TOKEN).build()
polling = UserPolling(api=API(VK_TOKEN))

chat_state = {}
        # self.tab = "    "

        # self.tg_prohibited_chars = [
        #     "_",
        #     "*",
        #     "[",
        #     "]",
        #     "(",
        #     ")",
        #     "~",
        #     "`",
        #     ">",
        #     "#",
        #     "+",
        #     "-",
        #     "=",
        #     "|",
        #     "{",
        #     "}",
        #     ".",
        #     "!",
        # ]
        # # self.message_types = ["user", "group", "chat"]
        # self.parse_mode = "MarkdownV2"

        # self.vk_message = None
        # self.attachments = None
        # self.conversation_name = None

        # self.message_text = None
        # self.answer = None

        # self.conversation_active = None
        # self.callback_data = None
        # self.reply_markup = None

        # # trailing stuff
        # self.trailing = None
        # self.tg_message_id = None
        # self.peer_id_previous = None

        # # talking to currently
        # self.active_conversation_id = None
        # self.active_conversation_name = None