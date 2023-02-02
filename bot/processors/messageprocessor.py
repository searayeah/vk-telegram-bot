import asyncio
from . import tg
from . import vk
class MessageProcessor:
    def __init__(self) -> None:
        pass

    async def process(self, event):
        asyncio.sleep(1)



message_processor = MessageProcessor()