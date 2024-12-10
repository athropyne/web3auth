import psycopg
import sqlalchemy.exc
from fastapi import Depends, HTTPException
from sqlalchemy import CursorResult
from starlette import status

from core.infrastructures import Database
from core.schema import accounts
from services.accounts.exc import AccountNotFound, AddressAlreadyExists


class Repository:
    def __init__(self,
                 database: Database = Depends(Database)):
        self.engine = database()

    async def create(self, data: dict):
        async with self.engine.connect() as c:
            try:
                cursor: CursorResult = await c.execute(
                    accounts.insert()
                    .values(data)
                    .returning(accounts)
                )
                await c.commit()
                return cursor.mappings().fetchone()
            except sqlalchemy.exc.IntegrityError as e:
                if isinstance(e.orig, psycopg.errors.UniqueViolation):
                    raise AddressAlreadyExists

    async def delete(self, address: str):
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(
                accounts.delete()
                .where(accounts.c.address == address)
                .returning(accounts)
            )
            if cursor.rowcount == 0:
                raise AccountNotFound
            await c.commit()
            return cursor.mappings().fetchone()

