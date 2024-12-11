from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from core import config
from services.security import dto
from services.security.dto import TokenResponseModel, AuthModel
from services.security.service import Service

router = APIRouter(prefix="/security", tags=["security"])


@router.get("/",
            response_model=dto.MessageForSignModel,
            status_code=status.HTTP_200_OK,
            description="Получить строку, которую необходимо подписать для авторизации")
async def get_message_for_sign():
    return dto.MessageForSignModel(message=config.settings.RAW_MESSAGE_FOR_SING)


@router.post("/",
             status_code=status.HTTP_200_OK,
             description="""Aутентифицирует пользователя по адресу и подписи. 
             ! Вместо username используйте адрес.
             ! Вместо password используйте подписанное сообщение""",
             response_model=TokenResponseModel
             )
async def auth(
        model: AuthModel,
        service: Service = Depends(Service)
):
    return await service.auth(model)
