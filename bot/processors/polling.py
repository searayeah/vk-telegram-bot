from . import tg
from . import vk
from bot.misc.keyboards import set_keyboard_1
from bot.misc.utils import fix_text
from vk_api.longpoll import Event, VkEventType
from bot import polling, state, TG_CHAT_ID


async def start_polling():
    async for event in polling.listen():
        for update in event.get("updates", []):
            event = Event(update)  # IMPORTANT change vkbottle longpoll version to 3
            # vk_api Event class works only with ver 3 longpoll
            # while vkbottle uses default version 0
            if (
                event.type == VkEventType.MESSAGE_NEW  # and event.to_me
            ):  # for testing purposes
                # logger.info(f"Entered new message")
                await process(event)


async def process(event):
    vk_message = await vk.get_message(event.message_id)
    state.trailing = state.trailing and state.peer_id_previous == vk_message.peer_id

    attachments = await vk.get_attachments(vk_message)

    if not state.trailing:
        state.conversation_name = f"_{await vk.get_name(vk_message.peer_id)}_"
        state.tg_message_text = "Chat with : " + state.conversation_name

    state.tg_message_text += "\n" + await vk.form_message(vk_message)

    conversation_is_active = state.active_conversation_id == vk_message.peer_id
    callback_data = f"{vk_message.peer_id}.{state.conversation_name}"

    reply_markup = (
        None if conversation_is_active else set_keyboard_1("Answer", callback_data)
    )

    if state.trailing:
        await tg.edit_message(
            state.tg_message_text, TG_CHAT_ID, state.tg_message_id, state.parse_mode, reply_markup
        )
    else:
        tg_message_id = await tg.send_message(
            state.tg_message_text, TG_CHAT_ID, state.parse_mode, reply_markup
        )
        state.tg_message_id = tg_message_id
        state.peer_id_previous = vk_message.peer_id
        state.trailing = True
