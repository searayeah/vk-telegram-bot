async def send_message(update, context):
    # if context.bot_data["message_processor"].active_conversation_id != None:
    #     await POLLING.api.messages.send(
    #         peer_id=context.bot_data["message_processor"].active_conversation_id,
    #         random_id=get_random_id(),
    #         message=update.message.text,
    #     )
    # else:
    await update.message.reply_text(text="No chat selected")
    # context.bot_data["message_processor"].trailing = False
