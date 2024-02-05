from fastapi import HTTPException
from pydantic.types import UUID
from starlette import status

from models.models import Dish_Pydantic
from repository.abstract_repository import AbstractRepository


class DishService:
    def __init__(self, dish_repo: type[AbstractRepository]):
        self.dish_repo: AbstractRepository = dish_repo()

    async def add_dish(self, submenu_id: UUID, dish: Dish_Pydantic):
        dish_dict = dish.dict()
        dish_dict['submenu_id'] = str(submenu_id)
        result_dish = await self.dish_repo.add_one(dish_dict)
        return result_dish

    async def update_dish(self, dish_id: UUID, dish: Dish_Pydantic):
        dish_dict = dish.dict()
        result_dish = await self.dish_repo.update_by_id(dish_id, dish_dict)
        return result_dish

    async def get_dishes(self):
        dishes = await self.dish_repo.find_all()
        return dishes

    async def get_dish_by_id(self, dish_id: UUID):
        dish = await self.dish_repo.find_one_by_id(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
        return dish

    async def delete_dish(self, dish_id: UUID):
        result = await self.dish_repo.delete_by_id(dish_id)
        return result
