from fastapi import APIRouter, Depends
from starlette import status

from core.security import TokenManager
from services.accounts.dto import CreateModel, ResponseCreatedModel
from services.accounts.service import Service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             description="добавляет новый адрес администратора если его еще нет",
             response_model=ResponseCreatedModel
             )
async def add(
        model: CreateModel,
        address: str = Depends(TokenManager.decode),
        service: Service = Depends(Service)
):
    return await service.create(model)


@router.delete("/{address}",
               status_code=status.HTTP_205_RESET_CONTENT,
               description="удаляет адрес если он есть и не корневой")
async def delete(
        address: str,
        service: Service = Depends(Service)
):
    return await service.delete(address)
