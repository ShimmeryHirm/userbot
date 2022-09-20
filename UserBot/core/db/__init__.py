import asyncio

from .db import init_db

async_session = asyncio.get_event_loop().run_until_complete(init_db())


async def load_db():
    """
    :return:
    """
    pass
