# from re import X
from vkbottle import UserPolling

# from vk_api.longpoll import VkLongPoll, VkEventType
import asyncio
from vkbottle import API
from vkbottle.user import User
import telegram
from vk_api.longpoll import Event, VkEventType
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from vk_api.utils import get_random_id


CURRENT_STATE = {
    "type": 0,  # 0 - no active chat, 1 - from_user # 2 - from_group, 3 - from_chat
    "id": 0,
    "name": "",
    "chat_name": "",
}



async def run_polling(polling, bot):
    async for event in polling.listen():
        for update in event.get("updates", []):
            event = Event(update)  # IMPORTANT change vkbottle longpoll version to 3
            # vk_api Event class works only with ver 3 longpoll
            # while vkbottle uses default version 0
            if event.type == VkEventType.MESSAGE_NEW:
                if event.from_user:
                    user_info = await polling.api.users.get(event.user_id)
                    output = (
                        f"{user_info[0].first_name} "
                        + f"{user_info[0].last_name}: {event.text}"
                    )
                    callback_object = (
                        f"1.{event.user_id}."
                        + f"{user_info[0].first_name} {user_info[0].last_name}."
                    )
                    keyboard = [
                        [InlineKeyboardButton("Answer", callback_data=callback_object)]
                    ]

                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await bot.send_message(
                        text=output, chat_id=MY_CHAT_ID, reply_markup=reply_markup
                    )
                elif event.from_group:
                    group_info = await polling.api.groups.get_by_id(event.group_id)
                    output = f"Сообщество {group_info[0].name}: {event.text}"

                    callback_object = f"2.{event.group_id}.{group_info[0].name}."
                    keyboard = [
                        [InlineKeyboardButton("Answer", callback_data=callback_object)]
                    ]

                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await bot.send_message(
                        text=output, chat_id=MY_CHAT_ID, reply_markup=reply_markup
                    )
                elif event.from_chat:
                    user_info = await polling.api.users.get(event.user_id)
                    chat_info = await polling.api.messages.get_conversations_by_id(
                        2000000000 + event.chat_id
                    )

                    output = (
                        f"Беседа {chat_info.items[0].chat_settings.title}"
                        + f"\n{user_info[0].first_name} "
                        + f"{user_info[0].last_name}: {event.text}"
                    )

                    callback_object = (
                        f"3.{2000000000 + event.chat_id}."
                        + f"{user_info[0].first_name} {user_info[0].last_name}."
                        + f"{chat_info.items[0].chat_settings.title}"
                    )
                    keyboard = [
                        [InlineKeyboardButton("Answer", callback_data=callback_object)]
                    ]

                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await bot.send_message(
                        text=output, chat_id=MY_CHAT_ID, reply_markup=reply_markup
                    )


async def answer_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    callback_data = query.data.split(".")
    CURRENT_STATE["type"] = int(callback_data[0])
    CURRENT_STATE["id"] = int(callback_data[1])
    CURRENT_STATE["name"] = callback_data[2]
    CURRENT_STATE["chat_name"] = callback_data[3]

    # context.user_data
    ## user context current chat
    if CURRENT_STATE["type"] == 1:
        output = f"Now talking with {CURRENT_STATE['name']}"
    elif CURRENT_STATE["type"] == 2:
        output = f"Now talking with group {CURRENT_STATE['name']}"
    elif CURRENT_STATE["type"] == 3:
        output = f"Now talking with chat {CURRENT_STATE['chat_name']}"

    await query.message.reply_text(text=output)


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CURRENT_STATE["type"] != 0:
        await polling.api.messages.send(
            peer_id=CURRENT_STATE["id"]
            if CURRENT_STATE["type"] in (1, 3)
            else -CURRENT_STATE["id"],
            random_id=get_random_id(),
            message=update.message.text,
        )
    else:
        await update.message.reply_text(text="No chat selected")


async def main():

    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CallbackQueryHandler(answer_button))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, send_message)
    )

    async with application:

        await application.updater.start_polling()
        await application.start()

        await run_polling(polling=polling, bot=application.bot)

        # run until it receives a stop signal
        await application.updater.stop()
        await application.stop()


polling = UserPolling(api=API(VK_TOKEN))
asyncio.run(main())
