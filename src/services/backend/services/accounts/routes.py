from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from core.security import TokenManager
from services.accounts.dto import CreateModel, ResponseCreatedModel
from services.accounts.service import Service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             description="добавляет новый адрес администратора если его еще нет",
             response_model=ResponseCreatedModel,
             dependencies=[Depends(TokenManager.decode)])
async def add(
        model: CreateModel,
        service: Service = Depends(Service)
):
    return await service.create(model)


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=List[str],
            description="получить список всех админских адресов",
            dependencies=[Depends(TokenManager.decode)])
async def get_list(
        service: Service = Depends(Service)
):
    return await service.get_list()


@router.delete("/{address}",
               status_code=status.HTTP_205_RESET_CONTENT,
               description="удаляет адрес если он есть и не корневой",
               dependencies=[Depends(TokenManager.decode)]
               )
async def delete(
        address: str,
        service: Service = Depends(Service)
):
    await service.delete(address)
