from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic.types import UUID
from starlette import status

from models.models import FullMenuPydantic, Menu_Pydantic
from routers.dependencies import menu_service
from services.menu_service import MenuService

menu_router = APIRouter(prefix='/api/v1/menus', tags=['menu'])


@menu_router.get('', response_model=list[Menu_Pydantic], status_code=status.HTTP_200_OK)
async def get_menu_list(_menu_service: Annotated[MenuService, Depends(menu_service)]) -> list[Menu_Pydantic]:
    menu_list = await _menu_service.get_menus()
    return menu_list


@menu_router.get('/{target_menu_id}', response_model=FullMenuPydantic, status_code=status.HTTP_200_OK)
async def get_menu_by_id(target_menu_id: UUID, _menu_service: Annotated[MenuService, Depends(menu_service)]) -> FullMenuPydantic:
    menu = await _menu_service.get_menu_by_id(target_menu_id)
    return menu


@menu_router.post('', response_model=Menu_Pydantic, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: Menu_Pydantic, _menu_service: Annotated[MenuService, Depends(menu_service)]) -> Menu_Pydantic:
    new_menu = await _menu_service.add_menu(menu)
    return new_menu


@menu_router.patch('/{target_menu_id}', response_model=Menu_Pydantic, status_code=status.HTTP_200_OK)
async def update_menu_by_id(new_menu: Menu_Pydantic, target_menu_id: UUID, _menu_service: Annotated[MenuService, Depends(menu_service)]) -> Menu_Pydantic:
    new_menu = await _menu_service.update_menu(target_menu_id, new_menu)
    return new_menu


@menu_router.delete('/{target_menu_id}', response_model=str, status_code=status.HTTP_200_OK)
async def delete_menu_by_id(target_menu_id: UUID, _menu_service: Annotated[MenuService, Depends(menu_service)]) -> str:
    response = await _menu_service.delete_menu(target_menu_id)
    return response
