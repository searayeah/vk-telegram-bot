from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
from vkbottle import API, UserPolling
from os import environ
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


load_dotenv()

TG_CHAT_ID = int(environ["TG_CHAT_ID"])
VK_TOKEN = environ["VK_TOKEN"]
TG_TOKEN = environ["TG_TOKEN"]


class State:
    parse_mode = "MarkdownV2"

    conversation_name = None

    trailing = None
    tg_message_id = None
    tg_message_text = None
    peer_id_previous = None

    active_conversation_id = None
    active_conversation_name = None


# self.message_types = ["user", "group", "chat"]


state = State()
application = ApplicationBuilder().token(TG_TOKEN).build()  # working on python 3.10+
polling = UserPolling(api=API(VK_TOKEN))
