import asyncio
from bot import application
from .processors.polling import start_polling
from .handlers import message, current, button, chats


async def main():
    async with application:
        await application.start()
        await application.updater.start_polling()

        await start_polling()

        await application.updater.stop()
        await application.stop()


asyncio.run(main())
