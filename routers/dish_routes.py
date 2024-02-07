from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic.types import UUID
from starlette import status

from models.models import CreateDishPydantic, Dish_Pydantic
from repository.response_errors import ResponseAlreadyTakenError, ResponseNotFoundError
from routers.dependencies import dish_service
from services.dish_service import DishService

dish_router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=['dish'])


@dish_router.get('', response_model=list[Dish_Pydantic], status_code=status.HTTP_200_OK, summary='Get all dishes')
async def get_dishes_list(_dish_service: Annotated[DishService, Depends(dish_service)]) -> list[Dish_Pydantic]:
    dish_list = await _dish_service.get_dishes()
    return dish_list


@dish_router.get('/{target_dish_id}', response_model=Dish_Pydantic,
                 status_code=status.HTTP_200_OK, summary='Get dish by id',
                 responses={status.HTTP_404_NOT_FOUND: {'description': 'Dish with given id was not found', 'model': ResponseNotFoundError}})
async def get_dish_by_id(target_dish_id: UUID,
                         _dish_service: Annotated[DishService, Depends(dish_service)]) -> Dish_Pydantic:
    dish = await _dish_service.get_dish_by_id(target_dish_id)
    return dish


@dish_router.post('', response_model=Dish_Pydantic, summary='Create new dish',
                  responses={status.HTTP_201_CREATED: {'description': 'Successful Response', 'model': Dish_Pydantic},
                             status.HTTP_400_BAD_REQUEST: {'description': 'Dish with given title already exists', 'model': ResponseAlreadyTakenError}},
                  status_code=status.HTTP_201_CREATED)
async def create_dish(dish: CreateDishPydantic, target_submenu_id: UUID,
                      _dish_service: Annotated[DishService, Depends(dish_service)]) -> Dish_Pydantic:
    new_dish = await _dish_service.add_dish(target_submenu_id, dish)
    return new_dish


@dish_router.patch('/{target_dish_id}', response_model=Dish_Pydantic, status_code=status.HTTP_200_OK,
                   summary='Change dish by id',
                   responses={status.HTTP_404_NOT_FOUND: {'description': 'Dish with given id was not found', 'model': ResponseNotFoundError},
                              status.HTTP_200_OK: {'description': 'Successful Response', 'model': Dish_Pydantic}})
async def update_dish_by_id(dish: Dish_Pydantic, target_dish_id: UUID,
                            _dish_service: Annotated[DishService, Depends(dish_service)]) -> Dish_Pydantic:
    new_dish = await _dish_service.update_dish(target_dish_id, dish)
    return new_dish


@dish_router.delete('/{target_dish_id}', response_model=str, status_code=status.HTTP_200_OK, summary='Delete dish by id')
async def delete_dish_by_id(target_dish_id: UUID, _dish_service: Annotated[DishService, Depends(dish_service)]) -> str:
    response: str = await _dish_service.delete_dish(target_dish_id)
    return response
