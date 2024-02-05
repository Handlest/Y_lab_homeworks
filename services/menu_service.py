from fastapi import HTTPException
from pydantic.types import UUID
from starlette import status

from models.models import Menu_Pydantic
from repository.abstract_repository import AbstractRepository


class MenuService:
    def __init__(self, menus_repo: type[AbstractRepository]):
        self.menus_repo: AbstractRepository = menus_repo()

    async def add_menu(self, menu: Menu_Pydantic):
        menu_dict = menu.dict()
        result_menu = await self.menus_repo.add_one(menu_dict)
        return result_menu

    async def update_menu(self, id: UUID, menu: Menu_Pydantic):
        menus_dict = menu.dict()
        result_menu = await self.menus_repo.update_by_id(id, menus_dict)
        return result_menu

    async def get_menus(self):
        menus = await self.menus_repo.find_all()
        return menus

    async def get_menu_by_id(self, menu_id: UUID):
        menu = (await self.menus_repo.find_one_by_id(menu_id)).fetchall()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        result_menu = menu[0][0]
        result_menu.submenus_count = menu[0][1]
        result_menu.dishes_count = menu[0][2]
        return result_menu

    async def delete_menu(self, menu_id: UUID):
        result = await self.menus_repo.delete_by_id(menu_id)
        return result
