from fastapi import Depends, HTTPException
from starlette import status

import core.config
from core.infrastructures import w3
from services.accounts.dto import CreateModel
from services.accounts.exc import InvalidAddress, DeleteRootAddress
from services.accounts.repository import Repository


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository)):
        self.repository = repository

    async def create(self, model: CreateModel):
        if not w3.is_address(model.address):
            raise InvalidAddress
        result = await self.repository.create(model.model_dump())
        return f"адрес {result['address']} успешно добавлен"

    async def delete(self, address: str):
        if address == core.config.settings.ROOT_ADDRESS:
            raise DeleteRootAddress
        result = await self.repository.delete(address)
        return f"адрес {result['address']} успешно удален"
