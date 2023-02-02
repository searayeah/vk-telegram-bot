from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
from vkbottle import API, UserPolling
from os import environ


load_dotenv()

TG_CHAT_ID = environ["TG_CHAT_ID"]
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


state = State()
application = ApplicationBuilder().token(TG_TOKEN).build()  # working on python 3.10+
polling = UserPolling(api=API(VK_TOKEN))