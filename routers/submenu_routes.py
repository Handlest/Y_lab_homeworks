from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic.types import UUID
from starlette import status

from models.models import FullSubmenuPydantic, Submenu_Pydantic
from routers.dependencies import submenu_service
from services.submenu_service import SubmenuService

submenu_router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus',
                           tags=['submenu'])


@submenu_router.get('', response_model=list[Submenu_Pydantic], status_code=status.HTTP_200_OK)
async def get_submenu_list(_submenu_service: Annotated[SubmenuService, Depends(submenu_service)]) -> list[Submenu_Pydantic]:
    submenu_list = await _submenu_service.get_submenus()
    return submenu_list


@submenu_router.get('/{target_submenu_id}', response_model=FullSubmenuPydantic)
async def get_submenu_by_id(target_submenu_id: UUID, _submenu_service: Annotated[SubmenuService, Depends(submenu_service)]) -> FullSubmenuPydantic:
    submenu = await _submenu_service.get_submenu_by_id(target_submenu_id)
    return submenu


@submenu_router.post('',
                     response_model=Submenu_Pydantic,
                     status_code=status.HTTP_201_CREATED)
async def create_submenu(submenu: Submenu_Pydantic, target_menu_id: UUID, _submenu_service: Annotated[SubmenuService, Depends(submenu_service)]) -> Submenu_Pydantic:
    new_submenu = await _submenu_service.add_submenu(target_menu_id, submenu)
    return new_submenu


@submenu_router.patch('/{target_submenu_id}',
                      response_model=Submenu_Pydantic,
                      status_code=status.HTTP_200_OK)
async def update_submenu_by_id(new_submenu: Submenu_Pydantic,
                               target_submenu_id: UUID, _submenu_service: Annotated[SubmenuService, Depends(submenu_service)]) -> Submenu_Pydantic:
    new_submenu = await _submenu_service.update_submenu(target_submenu_id, new_submenu)
    return new_submenu


@submenu_router.delete('/{target_submenu_id}', response_model=str)
async def delete_submenu_by_id(target_submenu_id: UUID, _submenu_service: Annotated[SubmenuService, Depends(submenu_service)]) -> str:
    response = await _submenu_service.delete_submenu(target_submenu_id)
    return response
