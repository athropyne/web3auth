from fastapi import Depends

import core.config
from core.infrastructures import w3
from services.accounts.dto import CreateModel
from services.accounts.exc import InvalidAddress, DeleteRootAddress
from services.accounts.repository import Repository
from services.accounts.dto import ResponseCreatedModel


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository)):
        self.repository = repository

    async def create(self, model: CreateModel):
        if not w3.is_address(model.address):
            raise InvalidAddress
        model.address = model.address.lower()
        result = await self.repository.create(model.model_dump())
        return ResponseCreatedModel(address=result['address'])

    async def delete(self, address: str):
        if address == core.config.settings.ROOT_ADDRESS:
            raise DeleteRootAddress
        if not w3.is_address(address):
            raise InvalidAddress
        result = await self.repository.delete(address.lower())

    async def get_list(self):
        return await self.repository.get_list()
