import asyncpg
import psycopg
import sqlalchemy.exc
import web3
from sqlalchemy import MetaData, CursorResult, select, exists
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection

from core import config
from core.config import logger
from core.schema import accounts


class Database:
    def __init__(self):
        s = config.settings
        self.engine = create_async_engine(
            f"postgresql+psycopg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_SOCKET}/{s.POSTGRES_DB}",
            echo=True)

    async def init(self, metadata: MetaData):
        async with self.engine.connect() as connection:
            # await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)
            await connection.commit()
            try:
                await self._minimum_fill(connection)
                await connection.commit()
            except sqlalchemy.exc.IntegrityError as e:
                await connection.rollback()
                if isinstance(e.orig, psycopg.errors.UniqueViolation):
                    logger.debug("корневой адрес уже существует")
                else:
                    raise Exception("Корневой адрес не создан")

        await self.engine.dispose()

    async def _check_root_address(self, connection: AsyncConnection):
        cursor: CursorResult = await connection.execute(
            select(accounts.c.address).
            where(accounts.c.address == config.settings.ROOT_ADDRESS)
        )

    async def _minimum_fill(self, connection: AsyncConnection):
        cursor: CursorResult = await connection.execute(
            accounts.insert()
            .values(address=config.settings.ROOT_ADDRESS)
        )

    async def dispose(self):
        await self.engine.dispose()

    def __call__(self) -> AsyncEngine:
        return self.engine


w3 = web3.Web3(web3.Web3.HTTPProvider(config.settings.ETH_NODE_HTTP_PROVIDER_URI))
