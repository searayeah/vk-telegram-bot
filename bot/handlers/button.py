


async def answer_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # callback_data = query.data.split(".")

    # context.bot_data["message_processor"].active_conversation_id = int(callback_data[0])
    # context.bot_data["message_processor"].active_conversation_name = callback_data[1]

    # output = f"Now talking with {context.bot_data['message_processor'].active_conversation_name}"
    # message = await query.message.reply_text(
    #     text=output, parse_mode=context.bot_data["message_processor"].parse_mode
    # )
    # await message.pin()
    # context.bot_data["message_processor"].trailing = False
