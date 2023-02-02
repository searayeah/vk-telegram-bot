from bot import application
from telegram.ext import CommandHandler

async def chats(update, context):
    await update.message.reply_text("chats")
    ## need review
    # chats = await POLLING.api.messages.get_conversations(count=10)
    # outputs = []
    # callbacks = []
    # # print(chats)
    # # print("test")

    # async def process_chat(i):
    #     print(chats.items[i].conversation.peer.type)
    #     if chats.items[i].conversation.peer.type == MessagesConversationPeerType.CHAT:
    #         print("CHAT CHAT")
    #         output = f"Беседа {chats.items[i].conversation.chat_settings.title}"
    #         callback_object = (
    #             f"chat.{chats.items[i].conversation.peer.id}."
    #             + f"{chats.items[i].conversation.chat_settings.title}"
    #         )
    #         return output, callback_object
    #     elif chats.items[i].conversation.peer.type == MessagesConversationPeerType.USER:
    #         print("USER USER")
    #         user_info = await POLLING.api.users.get(chats.items[i].conversation.peer.id)
    #         output = f"{user_info[0].first_name} " + f"{user_info[0].last_name}"
    #         callback_object = (
    #             f"user.{chats.items[i].conversation.peer.id}."
    #             + f"{user_info[0].first_name} {user_info[0].last_name}"
    #         )
    #         return output, callback_object
    #     elif (
    #         chats.items[i].conversation.peer.type == MessagesConversationPeerType.GROUP
    #     ):
    #         group_info = await POLLING.api.groups.get_by_id(
    #             abs(chats.items[i].conversation.peer.id)
    #         )
    #         output = f"Сообщество {group_info[0].name}"
    #         callback_object = (
    #             f"group.{abs(chats.items[i].conversation.peer.id)}.{group_info[0].name}"
    #         )
    #         return output, callback_object

    # outputs = await asyncio.gather(*[process_chat(i) for i in range(8)])
    # outputs = [item for sublist in outputs for item in sublist]

    # reply_markup = set_keyboard_8(*(outputs[::2] + outputs[1::2]))
    # await update.message.reply_text(
    #     text=f"Непрочитанных: {chats.unread_count}",
    #     reply_markup=reply_markup,
    # )
    # print(chats)
    # TRAILING_STATE["active"] = False

application.add_handler(CommandHandler("now", chats))
