from bot.misc.keyboards import set_keyboard_1
from vk_api.utils import get_random_id
# import bot.processors.vk



async def process(self, event):
    import asyncio

    print("Processed")
    await asyncio.sleep(1)

    # async def set(self, event):
    #     # TO-DO
    #     # кейс когда идет реплай на группу пересланных сообщений
    #     # message edit рассмотреть
    #     # 4096 UTF8 characters макс длина сообщения в телеге
    #     # если пригласили в беседу
    #     # если поменяли название беседы
    #     # стикер
    #     # attachments
    #     # fix text for \n and stuff
    #     # if youtube video is sent
    #     # if attachments number is more than one
    #     # скинули новость

    #     self.vk_message = (
    #         await self.vk_polling.api.messages.get_by_id(event.message_id)
    #     ).items[0]

    #     # self.attachments = await self.get_attachments(self.vk_message)

    #     # tg trailing message
    #     self.trailing = (
    #         self.trailing and self.peer_id_previous == self.vk_message.peer_id
    #     )

    #     if not self.trailing:
    #         self.conversation_name = f"_{await self.get_name(self.vk_message.peer_id)}_"
    #         self.answer = "Chat with : " + self.conversation_name

    #     self.message_text = await self.form_message(self.vk_message)
    #     self.answer += "\n" + self.message_text

    #     self.conversation_active = (
    #         self.active_conversation_id == self.vk_message.peer_id
    #     )
    #     self.callback_data = f"{self.vk_message.peer_id}.{self.conversation_name}"
    #     self.reply_markup = (
    #         None
    #         if self.conversation_active
    #         else set_keyboard_1("Answer", self.callback_data)
    #     )

    # async def send_msg(self):
    #     if self.trailing:
    #         await self.bot.edit_message_text(
    #             text=self.answer,
    #             chat_id=self.tg_chat_id,
    #             message_id=self.tg_message_id,
    #             parse_mode=self.parse_mode,
    #             reply_markup=self.reply_markup,
    #         )
    #     else:
    #         message = await self.bot.send_message(
    #             text=self.answer,
    #             chat_id=self.tg_chat_id,
    #             parse_mode=self.parse_mode,
    #             reply_markup=self.reply_markup,
    #         )
    #         self.tg_message_id = message.message_id
    #         self.peer_id_previous = self.vk_message.peer_id
    #         self.trailing = True

    # async def form_message(self, message, level=0):
    #     text = await self.get_message_text(message, level)
    #     reply_message = await self.get_reply_message(message, level)
    #     forwarded_messages = await self.get_forwarded_messages(message, level)
    #     output = [text, reply_message, forwarded_messages]
    #     return "\n".join([x for x in output if x])

    # async def get_message_text(self, message, level=0):
    #     name = await self.get_name(message.from_id)
    #     if message.text:
    #         return f"{self.set_tab(level)}*{name}*: {self.fix_text(message.text)}"
    #     else:
    #         return f"{self.set_tab(level)}*{name}*: Нет текста сообщения"

    # async def get_reply_message(self, message, level=0):
    #     if message.reply_message:
    #         text = await self.get_message_text(message.reply_message, level + 1)
    #         return f"{self.set_tab(level)}_В ответ на:_\n{text}"
    #     else:
    #         return ""

    # async def get_forwarded_messages(self, message, level=0):
    #     forwarded_messages_text = ""
    #     if message.fwd_messages:
    #         forwarded_messages_text += f"{self.set_tab(level)}_Пересланные сообщения_"
    #         for message in message.fwd_messages:
    #             forwarded_messages_text += "\n" + await self.form_message(
    #                 message, level + 1
    #             )
    #     return forwarded_messages_text



    # def set_tab(self, level):
    #     return self.tab * level

    # async def process(self, event):
    #     await self.set(event)
    #     await self.send_msg()
    #     print(self.__dict__)

    # def now(self):
    #     output = {
    #         "text": f"Now talking with {self.active_conversation_name}",
    #         "parse_mode": self.parse_mode,
    #     }
    #     self.trailing = False
    #     return output

    # def send_message(self, message_text):
    #     output = {}
    #     if self.active_conversation_id:
    #         output = {"peer_id":self.active_conversation_id,
    #         "random_id":get_random_id(),
    #         "message":message_text}
    #     else:
    #         output = {"text":"No chat selected"}
    #         await update.message.reply_text(text="No chat selected")
    #     self.trailing = False



