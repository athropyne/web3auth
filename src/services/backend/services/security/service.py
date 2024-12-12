from eth_account.messages import encode_defunct
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

import core.config
from core.infrastructures import w3
from core.security import TokenManager, TokenTypes
from services.security.dto import TokenResponseModel, AuthModel
from services.security.exc import InvalidAddress, InvalidSignature, AddressNotFound
from services.security.repository import Repository
from core.config import logger


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository)):
        self.repository = repository

    async def auth(self, model: AuthModel):
        logger.debug(f"проверка адреса {model.address}")
        if not w3.is_address(model.address):
            raise InvalidAddress
        logger.debug(f"адрес провалидирован")
        signable_message = encode_defunct(text=model.message)
        recovered_address = w3.eth.account.recover_message(signable_message, signature=model.signature)
        logger.debug(f"восстановленный адрес {recovered_address}")
        if recovered_address.lower() != model.address.lower():
            logger.debug("адреса не совпадают")
            raise InvalidSignature
        result = await self.repository.check_address(recovered_address.lower())
        if result is not None:
            logger.debug(f"адрес {result} присутствует в базе")
            access_token = TokenManager.create({"sub": result}, TokenTypes.ACCESS)
            return TokenResponseModel(
                access_token=access_token,
                token_type="Bearer",
                refresh_token=""
            )
        else:
            logger.debug(f"адрес {recovered_address} отсутствует в базе")
            raise AddressNotFound
