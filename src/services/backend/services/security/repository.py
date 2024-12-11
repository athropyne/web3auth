from fastapi import Depends
from sqlalchemy import CursorResult, select

from core.infrastructures import Database
from core.schema import accounts


class Repository:
    def __init__(self,
                 database: Database = Depends(Database)):
        self.engine = database()

    async def check_address(self, address: str):
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(
                select(accounts.c.address)
                .where(accounts.c.address == address)
            )
            return cursor.scalar()
