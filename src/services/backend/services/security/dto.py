from pydantic import BaseModel

class AuthModel(BaseModel):
    address: str
    message: str
    signature: str

class MessageForSignModel(BaseModel):
    message: str


class TokenResponseModel(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
