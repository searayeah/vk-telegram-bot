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
from bot import polling#, message_processor
# from bot.processors.messageprocessor import process





async def get_name(peer_id):
    
    await asyncio.sleep(1)
    # type = get_message_type(peer_id)
    # if type == "group":
    #     group_info = await polling.api.groups.get_by_id(abs(peer_id))
    #     return fix_text(group_info[0].name)
    # elif type == "user":
    #     user_info = await polling.api.users.get(peer_id)
    #     return fix_text(f"{user_info[0].first_name} {user_info[0].last_name}")
    # elif type == "chat":
    #     chat_info = await polling.api.messages.get_conversations_by_id(
    #         peer_id
    #     )
    #     return fix_text(chat_info.items[0].chat_settings.title)



def send_attach():
    pass


def send_vid():
    pass
