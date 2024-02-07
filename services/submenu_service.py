import json

import aioredis
from aioredis import Redis
from fastapi import HTTPException
from pydantic.types import UUID
from starlette import status

from models.models import Submenu_Pydantic
from repository.abstract_repository import AbstractRepository


class SubmenuService:
    def __init__(self, submenus_repo: type[AbstractRepository]):
        self.submenus_repo: AbstractRepository = submenus_repo()
        self.redis: Redis = aioredis.from_url('redis://redis/1')

    async def add_submenu(self, menu_id: UUID, submenu: Submenu_Pydantic):
        submenu_dict = submenu.dict()
        submenu_dict['menu_id'] = menu_id
        db_submenu = await self.submenus_repo.find_one_by_title(submenu_dict['title'])
        if db_submenu:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='submenu with given title already exists')
        result_submenu = await self.submenus_repo.add_one(submenu_dict)
        redis_menu = submenu_dict
        redis_menu['menu_id'] = str(redis_menu['menu_id'])
        redis_menu['dishes_count'] = 0
        await self.redis.set(str(result_submenu.id), json.dumps(redis_menu))
        return result_submenu

    async def update_submenu(self, submenu_id: UUID, submenu: Submenu_Pydantic):
        submenu_dict = submenu.dict()
        await self.redis.delete(str(submenu_id))
        db_submenu = (await self.submenus_repo.find_one_by_id(submenu_id)).fetchall()
        if not db_submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        result_submenu = await self.submenus_repo.update_by_id(submenu_id, submenu_dict)
        return result_submenu

    async def get_submenus(self):
        submenus = await self.submenus_repo.find_all()
        return submenus

    async def get_submenu_by_id(self, submenu_id: UUID):
        redis_menu = await self.redis.get(str(submenu_id))
        if redis_menu is not None:
            redis_menu = json.loads(redis_menu)
            redis_menu['id'] = submenu_id
            return redis_menu
        submenu = (await self.submenus_repo.find_one_by_id(submenu_id)).fetchall()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        result_submenu = submenu[0][0].as_dict()
        result_submenu['dishes_count'] = submenu[0][1]
        await self.redis.set(str(result_submenu['id']), json.dumps(result_submenu))
        return result_submenu

    async def delete_submenu(self, submenu_id: UUID):
        await self.redis.delete(str(submenu_id))
        result = await self.submenus_repo.delete_by_id(submenu_id)
        return result
