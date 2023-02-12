from bot import application
from telegram.ext import CallbackQueryHandler
from bot import state


async def answer_button(update, context):
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split(".")

    state.active_conversation_id = int(callback_data[1])
    # state.active_conversation_name = callback_data[1]

    text = f"Now talking with {'test'}"
    message = await query.message.reply_text(text=text, parse_mode=state.parse_mode)
    await message.pin()

    state.trailing = False


application.add_handler(CallbackQueryHandler(answer_button))
