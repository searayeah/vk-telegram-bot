# 4096 UTF8 characters
import asyncio
from re import A
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
from itertools import compress
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

TG_CHAT_ID = os.environ["TG_CHAT_ID"]
VK_TOKEN = os.environ["VK_TOKEN"]
TG_TOKEN = os.environ["TG_TOKEN"]




POLLING = UserPolling(api=API(VK_TOKEN))

shitty_chars = [
    "_",
    "*",
    "[",
    "]",
    "(",
    ")",
    "~",
    "`",
    ">",
    "#",
    "+",
    "-",
    "=",
    "|",
    "{",
    "}",
    ".",
    "!",
]


class MessageProcessor:
    def __init__(self, bot):
        self.bot = bot

        self.message_types = ["user", "group", "chat"]
        self.parse_mode = "MarkdownV2"

        self.trailing = None
        self.message_id = None
        self.id = None
        self.message_text = None
        self.name = None
        self.peer_id = None
        self.chat_active = None
        self.callback_data = None
        self.reply_markup = None

        # talking to currently
        self.answer_type = None
        self.answer_id = None
        self.answer_name = None

    async def set(self, event):
        # кейс когда идет реплай на группу пересланных сообщений
        self.vk_message_id = event.message_id
        self.vk_message = (
            await POLLING.api.messages.get_by_id(self.vk_message_id)
        ).items[0]
        self.reply_text = await self.get_reply_message(self.vk_message)
        self.forwarded_messages = await self.get_fwd_messages(self.vk_message)
        self.peer_id = event.peer_id
        self.message_type, self.id, self.trailing = self.get_event_info(event)
        self.name = (
            self.name
            if self.trailing
            else await self.get_name(self.message_type, self.id)
        )
        self.message_id = self.message_id if self.trailing else None

        self.chat_user = (
            f"*{await self.get_name('user', event.user_id)}: *"
            if self.message_type == "chat"
            else ""
        )

        self.message_text = (
            f"{self.message_text}\n{self.chat_user}{self.fix_text(event.text)}{self.reply_text}{self.forwarded_messages}"
            if self.trailing
            else f"{self.chat_user}{self.fix_text(event.text)}{self.reply_text}{self.forwarded_messages}"  # иногда сюда заходит почему то
        )

        self.answer = (
            f"_{self.name}_\n{self.message_text}"
            if self.message_type == "chat"
            else f"*{self.name}*: {self.message_text}"
        )

        self.chat_active = self.answer_id == self.peer_id
        self.callback_data = f"{self.message_type}.{self.peer_id}.{self.name}"
        self.reply_markup = (
            set_keyboard_1("Answer", self.callback_data)
            if not self.chat_active
            else None
        )

    async def get_name(self, message_type, id):
        if message_type == "group":
            group_info = await POLLING.api.groups.get_by_id(id)
            return self.fix_text(group_info[0].name)
        elif message_type == "user":
            user_info = await POLLING.api.users.get(id)
            return self.fix_text(f"{user_info[0].first_name} {user_info[0].last_name}")
        elif message_type == "chat":
            chat_info = await POLLING.api.messages.get_conversations_by_id(
                int(2e9) + id
            )
            return self.fix_text(chat_info.items[0].chat_settings.title)

    def get_event_info(self, event):
        if event.from_user:
            return "user", event.user_id, self.trailing and self.id == event.user_id
        elif event.from_group:
            return "group", event.group_id, self.trailing and self.id == event.group_id
        elif event.from_chat:
            return "chat", event.chat_id, self.trailing and self.id == event.chat_id

    async def send_msg(self):
        if self.trailing:
            await self.bot.edit_message_text(
                text=self.answer,
                chat_id=TG_CHAT_ID,
                message_id=self.message_id,
                parse_mode=self.parse_mode,
                reply_markup=self.reply_markup,
            )
        else:
            message = await self.bot.send_message(
                text=self.answer,
                chat_id=TG_CHAT_ID,
                parse_mode=self.parse_mode,
                reply_markup=self.reply_markup,
            )
            self.message_id = message.message_id
            self.trailing = True

    async def get_reply_message(self, message, level=0):
        if message.reply_message:
            name = await self.get_name(
                "user" if message.reply_message.from_id > 0 else "group",
                abs(message.reply_message.from_id),
            )
            return f"\n{'    '*level}_В ответ на:_\n{'    '*(level+1)}{name}: {self.fix_text(message.reply_message.text)}"
        else:
            return ""

    ## какая то хуйня нейминг надо исправить
    async def get_fwd_messages(self, vk_message, level=0, skip_first=True):
        future_text = ""
        if vk_message.fwd_messages:
            future_text += f"{'    '*level}_Пересланные сообщения_\n"
            for message in vk_message.fwd_messages:
                future_text += await self.get_fwd_messages(message, level + 1)
        if skip_first and level == 0:
            return f"\n{future_text}" if future_text != "" else ""
        else:
            name = await self.get_name(
                "user" if vk_message.from_id > 0 else "group", abs(vk_message.from_id)
            )
            reply_message = await self.get_reply_message(vk_message, level)
            return f"{'    '*level}{name} : {self.fix_text(vk_message.text)}{reply_message}\n{future_text}"

    def fix_text(self, text):
        if len(text) == 0:
            return "Нет текста сообщения"  # а если фотография???))
        text = (
            text.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&amp;", "&")
        )
        for char in shitty_chars:
            text = text.replace(char, f"\\{char}")
        return text

    async def process(self, event):
        await self.set(event)
        await self.send_msg()
        print(self.__dict__)


async def run_polling(context):
    async for event in POLLING.listen():
        for update in event.get("updates", []):
            event = Event(update)  # IMPORTANT change vkbottle longpoll version to 3
            # vk_api Event class works only with ver 3 longpoll
            # while vkbottle uses default version 0
            if (
                event.type == VkEventType.MESSAGE_NEW
            ):  # and event.to_me:  # for testing purposes
                logger.info(f"Entered new message")
                await context["message_processor"].process(event)


async def answer_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split(".")

    context.bot_data["message_processor"].answer_type = callback_data[0]
    context.bot_data["message_processor"].answer_id = int(callback_data[1])
    context.bot_data["message_processor"].answer_name = callback_data[2]

    output = f"Now talking with {context.bot_data['message_processor'].answer_name}"
    message = await query.message.reply_text(text=output)
    await message.pin()
    context.bot_data["message_processor"].trailing = False


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot_data["message_processor"].answer_type != None:
        await POLLING.api.messages.send(
            peer_id=context.bot_data["message_processor"].answer_id,
            random_id=get_random_id(),
            message=update.message.text,
        )
    else:
        await update.message.reply_text(text="No chat selected")
    context.bot_data["message_processor"].trailing = False


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = f"Now talking with {context.bot_data['message_processor'].answer_name}"
    await update.message.reply_text(text=output)
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

    application.bot_data["message_processor"] = MessageProcessor(application.bot)
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
