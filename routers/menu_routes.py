from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic.types import UUID
from starlette import status

from models.models import Menu_Pydantic
from routers.dependencies import menu_service
from services.menu_service import MenuService

menu_router = APIRouter(prefix='/api/v1/menus', tags=['menu'])


@menu_router.get('')
async def get_menu_list(menu_service: Annotated[MenuService, Depends(menu_service)]):
    menu_list = await menu_service.get_menus()
    return menu_list


@menu_router.get('/{target_menu_id}')
async def get_menu_by_id(target_menu_id: UUID, menu_service: Annotated[MenuService, Depends(menu_service)]):
    menu = await menu_service.get_menu_by_id(target_menu_id)
    return menu


@menu_router.post('', response_model=Menu_Pydantic, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: Menu_Pydantic, menu_service: Annotated[MenuService, Depends(menu_service)]):
    new_menu = await menu_service.add_menu(menu)
    return new_menu


@menu_router.patch('/{target_menu_id}', response_model=Menu_Pydantic)
async def update_menu_by_id(new_menu: Menu_Pydantic, target_menu_id: UUID, menu_service: Annotated[MenuService, Depends(menu_service)]):
    new_menu = await menu_service.update_menu(target_menu_id, new_menu)
    return new_menu


@menu_router.delete('/{target_menu_id}')
async def delete_menu_by_id(target_menu_id: UUID, menu_service: Annotated[MenuService, Depends(menu_service)]):
    response = await menu_service.delete_menu(target_menu_id)
    return response
