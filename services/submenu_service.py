from fastapi import HTTPException
from pydantic.types import UUID
from starlette import status

from models.models import Submenu_Pydantic
from repository.abstract_repository import AbstractRepository


class SubmenuService:
    def __init__(self, submenus_repo: type[AbstractRepository]):
        self.submenus_repo: AbstractRepository = submenus_repo()

    async def add_submenu(self, menu_id: UUID, submenu: Submenu_Pydantic):
        submenu_dict = submenu.dict()
        submenu_dict['menu_id'] = menu_id
        result_submenu = await self.submenus_repo.add_one(submenu_dict)
        return result_submenu

    async def update_submenu(self, submenu_id: UUID, submenu: Submenu_Pydantic):
        submenu_dict = submenu.dict()
        result_submenu = await self.submenus_repo.update_by_id(submenu_id, submenu_dict)
        return result_submenu

    async def get_submenus(self):
        submenus = await self.submenus_repo.find_all()
        return submenus

    async def get_submenu_by_id(self, submenu_id: UUID):
        submenu = (await self.submenus_repo.find_one_by_id(submenu_id)).fetchall()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        result_submenu = submenu[0][0]
        result_submenu.dishes_count = submenu[0][1]
        return result_submenu

    async def delete_submenu(self, submenu_id: UUID):
        result = await self.submenus_repo.delete_by_id(submenu_id)
        return result
