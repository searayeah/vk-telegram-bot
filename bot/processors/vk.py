from vk_api.longpoll import Event, VkEventType
from vk_api.utils import get_random_id
from vkbottle import API, UserPolling
from vkbottle.user import User
from vkbottle_types.objects import MessagesConversationPeerType
from bot import polling

from bot.misc.utils import get_message_type, fix_text, set_tab


async def get_attachments(message_id):
    pass


async def send_message(peer_id, text):
    await polling.api.messages.send(
        peer_id=peer_id,
        random_id=get_random_id(),
        message=text,
    )


async def get_message(message_id):
    message = (await polling.api.messages.get_by_id(message_id)).items[0]
    return message


async def get_name(peer_id):
    type = get_message_type(peer_id)
    if type == "group":
        group_info = await polling.api.groups.get_by_id(abs(peer_id))
        return fix_text(group_info[0].name)
    elif type == "user":
        user_info = await polling.api.users.get(peer_id)
        return fix_text(f"{user_info[0].first_name} {user_info[0].last_name}")
    elif type == "chat":
        chat_info = await polling.api.messages.get_conversations_by_id(peer_id)
        return fix_text(chat_info.items[0].chat_settings.title)


async def form_message(message, level=0):
    text = await get_message_text(message, level)
    reply_message = await get_reply_message(message, level)
    forwarded_messages = await get_forwarded_messages(message, level)
    output = [text, reply_message, forwarded_messages]
    return "\n".join([x for x in output if x])


async def get_message_text(message, level=0):
    name = await get_name(message.from_id)
    if message.text:
        return f"{set_tab(level)}*{name}*: {fix_text(message.text)}"
    else:
        return f"{set_tab(level)}*{name}*: Нет текста сообщения"


async def get_reply_message(message, level=0):
    if message.reply_message:
        text = await get_message_text(message.reply_message, level + 1)
        return f"{set_tab(level)}_В ответ на:_\n{text}"
    else:
        return ""


async def get_forwarded_messages(message, level=0):
    forwarded_messages_text = ""
    if message.fwd_messages:
        forwarded_messages_text += f"{set_tab(level)}_Пересланные сообщения_"
        for message in message.fwd_messages:
            forwarded_messages_text += "\n" + await form_message(message, level + 1)
    return forwarded_messages_text


def send_attach():
    pass


def send_vid():
    pass


async def get_chats(count, offset):
    chats = await polling.api.messages.get_conversations(
        count=count, extended=True, offset=offset
    )
    data = {}
    for item in chats.items:
        if item.conversation.peer.type == MessagesConversationPeerType.USER:
            for profile in chats.profiles:
                if profile.id == item.conversation.peer.id:
                    name = f"{profile.first_name} {profile.last_name}"
                    break
        elif item.conversation.peer.type == MessagesConversationPeerType.GROUP:
            for group in chats.groups:
                if group.id == abs(item.conversation.peer.id):
                    name = group.name
                    break
        elif item.conversation.peer.type == MessagesConversationPeerType.CHAT:
            name = item.conversation.chat_settings.title
        data[item.conversation.peer.id] = name # do not require fix_text as keyboard buttons don't support MarkDown
        if item.conversation.unread_count:
            data[item.conversation.peer.id] += item.conversation.unread_count
    unread_count = chats.unread_count if chats.unread_count else 0
    chats_count = chats.count if chats.count else 0
    return chats_count, unread_count, data
