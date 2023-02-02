from bot import application


async def edit_message(text, chat_id, message_id, parse_mode=None, reply_markup=None):
    await application.bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=message_id,
        parse_mode=parse_mode,
        reply_markup=reply_markup,
    )


async def send_message(text, chat_id, parse_mode=None, reply_markup=None):
    message = await application.bot.send_message(
        text=text,
        chat_id=chat_id,
        parse_mode=parse_mode,
        reply_markup=reply_markup,
    )
    return message.message_id


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
