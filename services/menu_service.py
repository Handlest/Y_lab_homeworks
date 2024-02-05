import json

import aioredis
from aioredis import Redis
from fastapi import HTTPException
from pydantic.types import UUID
from starlette import status

from models.models import Menu, Menu_Pydantic
from repository.abstract_repository import AbstractRepository


class MenuService:
    def __init__(self, menus_repo: type[AbstractRepository]):
        self.menus_repo: AbstractRepository = menus_repo()
        self.redis: Redis = aioredis.from_url('redis://redis/1')

    async def add_menu(self, menu: Menu_Pydantic):
        menu_dict = menu.dict()
        result_menu = await self.menus_repo.add_one(menu_dict)
        redis_menu = menu_dict
        redis_menu['submenus_count'] = 0
        redis_menu['dishes_count'] = 0
        await self.redis.set(str(result_menu.id), json.dumps(redis_menu))
        return result_menu

    async def update_menu(self, id: UUID, menu: Menu_Pydantic):
        menus_dict = menu.dict()
        await self.redis.delete(str(id))
        result_menu = await self.menus_repo.update_by_id(id, menus_dict)
        return result_menu

    async def get_menus(self):
        menus = await self.menus_repo.find_all()
        return menus

    async def get_menu_by_id(self, menu_id: UUID):
        redis_menu = await self.redis.get(str(menu_id))
        if redis_menu is not None:
            redis_menu = json.loads(redis_menu)
            redis_menu['id'] = menu_id
            return redis_menu
        menu = (await self.menus_repo.find_one_by_id(menu_id)).fetchall()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        result_menu: Menu = menu[0][0].as_dict()
        result_menu['submenus_count'] = menu[0][1]
        result_menu['dishes_count'] = menu[0][2]
        await self.redis.set(str(result_menu['id']), json.dumps(result_menu))
        return result_menu

    async def delete_menu(self, menu_id: UUID):
        await self.redis.delete(str(menu_id))
        result = await self.menus_repo.delete_by_id(menu_id)
        return result
