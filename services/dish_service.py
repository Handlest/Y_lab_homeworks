import json

import aioredis
from aioredis import Redis
from fastapi import HTTPException
from pydantic.types import UUID
from starlette import status

from models.models import Dish_Pydantic
from repository.abstract_repository import AbstractRepository


class DishService:
    def __init__(self, dish_repo: type[AbstractRepository]):
        self.dish_repo: AbstractRepository = dish_repo()
        self.redis: Redis = aioredis.from_url('redis://redis/1')

    async def add_dish(self, submenu_id: UUID, dish: Dish_Pydantic):
        dish_dict = dish.dict()
        dish_dict['submenu_id'] = str(submenu_id)
        db_dish = await self.dish_repo.find_one_by_title(dish_dict['title'])
        if db_dish:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='dish with given title already exists')
        result_dish = await self.dish_repo.add_one(dish_dict)
        await self.redis.set(str(result_dish.id), json.dumps(result_dish.as_dict()))
        return result_dish

    async def update_dish(self, dish_id: UUID, dish: Dish_Pydantic):
        dish_dict = dish.dict()
        await self.redis.delete(str(dish_id))
        db_dish = await self.dish_repo.find_one_by_id(dish_id)
        if not db_dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
        result_dish = await self.dish_repo.update_by_id(dish_id, dish_dict)
        return result_dish

    async def get_dishes(self):
        dishes = await self.dish_repo.find_all()
        return dishes

    async def get_dish_by_id(self, dish_id: UUID):
        redis_dish = await self.redis.get(str(dish_id))
        if redis_dish is not None:
            redis_dish = json.loads(redis_dish)
            redis_dish['id'] = dish_id
            return redis_dish
        dish = await self.dish_repo.find_one_by_id(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
        await self.redis.set(str(dish.id), json.dumps(dish.as_dict()))
        return dish

    async def delete_dish(self, dish_id: UUID):
        await self.redis.delete(str(dish_id))
        result = await self.dish_repo.delete_by_id(dish_id)
        return result
