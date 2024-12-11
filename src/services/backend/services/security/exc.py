from fastapi import HTTPException
from starlette import status


class InvalidAddress(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="неверный адрес. проверьте все символы еще раз."
        )


class InvalidSignature(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="неверная подпись"
        )


class AddressNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="вы не админ"
        )
