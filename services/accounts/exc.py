from fastapi import HTTPException
from starlette import status


class InvalidAddress(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="неверный адрес. проверьте все символы еще раз."
        )


class DeleteRootAddress(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="невозможно удалить корневой адрес"
        )


class AccountNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="адрес не найден"
        )


class AddressAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="адрес уже существует"
        )
