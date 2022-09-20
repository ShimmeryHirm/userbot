from asyncio import current_task

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import PSQL_DB, PSQL_HOST, PSQL_PASSWORD, PSQL_PORT, PSQL_USER
from core.db.tables import METADATA


async def init_db():
    """
    LGTM!
    :return:
    """
    url = URL.create(drivername='postgresql+asyncpg',
                     username=PSQL_USER,
                     password=PSQL_PASSWORD,
                     host=PSQL_HOST,
                     port=PSQL_PORT,
                     database=PSQL_DB)
    engine = create_async_engine(url, echo=False)

    # async with engine.begin() as conn:
    #     await conn.run_sync(METADATA.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(METADATA.create_all)

    async_session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async_session = async_scoped_session(async_session_factory, scopefunc=current_task)
    return async_session
