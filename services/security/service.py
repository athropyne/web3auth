from eth_account.datastructures import SignedMessage
from eth_account.messages import encode_defunct
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import core.config
from core.infrastructures import w3
from core.security import TokenManager, TokenTypes
from services.security.dto import TokenResponseModel
from services.security.exc import InvalidAddress, InvalidSignature
from services.security.repository import Repository


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository)):
        self.repository = repository

    async def auth(self, form: OAuth2PasswordRequestForm):
        if not w3.is_address(form.username):
            raise InvalidAddress
        signable_message = encode_defunct(text=core.config.settings.RAW_MESSAGE_FOR_SING)
        recovered_address = w3.eth.account.recover_message(signable_message, signature=signed_message.signature)
        if recovered_address.lower() != form.username.lower():
            raise InvalidSignature
        result = await self.repository.check_address(recovered_address)
        if result is not None:
            access_token = TokenManager.create({"sub": "result"}, TokenTypes.ACCESS)
            return TokenResponseModel(
                access_token=access_token,
                token_type="Bearer",
                refresh_token=""
            )
        else:
            raise
