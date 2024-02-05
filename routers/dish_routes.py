from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic.types import UUID
from starlette import status

from models.models import Dish_Pydantic
from routers.dependencies import dish_service
from services.dish_service import DishService

dish_router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=['dish'])


@dish_router.get('')
async def get_dishes_list(dish_service: Annotated[DishService, Depends(dish_service)]):
    dish_list = await dish_service.get_dishes()
    return dish_list


@dish_router.get('/{target_dish_id}')
async def get_dish_by_id(target_dish_id: UUID, dish_service: Annotated[DishService, Depends(dish_service)]):
    dish = await dish_service.get_dish_by_id(target_dish_id)
    return dish


@dish_router.post('', response_model=Dish_Pydantic,
                  status_code=status.HTTP_201_CREATED)
async def create_dish(dish: Dish_Pydantic, target_submenu_id: UUID, dish_service: Annotated[DishService, Depends(dish_service)]):
    new_dish = await dish_service.add_dish(target_submenu_id, dish)
    return new_dish


@dish_router.patch('/{target_dish_id}',
                   response_model=Dish_Pydantic)
async def update_dish_by_id(dish: Dish_Pydantic, target_dish_id: UUID, dish_service: Annotated[DishService, Depends(dish_service)]):
    new_dish = await dish_service.update_dish(target_dish_id, dish)
    return new_dish


@dish_router.delete('/{target_dish_id}')
async def delete_dish_by_id(target_dish_id: UUID, dish_service: Annotated[DishService, Depends(dish_service)]):
    response = await dish_service.delete_dish(target_dish_id)
    return response
