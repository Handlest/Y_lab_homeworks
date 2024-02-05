from pydantic.types import UUID
from sqlalchemy import func, select

from config import async_session
from models.models import Dish, Menu, Submenu
from repository.abstract_repository import SQLAlchemyRepository


class MenuRepository(SQLAlchemyRepository):
    model = Menu

    async def find_one_by_id(self, id: UUID):
        async with async_session() as session:
            dishes_stmt = select(func.count(Dish.id)).join(Submenu).where(Submenu.menu_id == id).scalar_subquery()
            submenus_stmt = select(func.count(Submenu.id)).where(Submenu.menu_id == id).scalar_subquery()
            final_stmt = select(self.model, submenus_stmt, dishes_stmt).where(self.model.id == id)
            res = await session.execute(final_stmt)
            await session.commit()
            return res


class SubmenuRepository(SQLAlchemyRepository):
    model = Submenu

    async def add_one(self, data: dict) -> dict:
        async with async_session() as session:
            new_instance = self.model(**data)
            session.add(new_instance)
            await session.commit()
            menu = (await session.execute(select(Menu).where(Submenu.menu_id == Menu.id))).scalars().first()
            await self.redis.delete(str(menu.id))
            return new_instance

    async def find_one_by_id(self, id: UUID):
        async with async_session() as session:
            dishes_stmt = select(func.count(Dish.id)).where(Dish.submenu_id == id).scalar_subquery()
            final_stmt = select(self.model, dishes_stmt).where(self.model.id == id)
            res = await session.execute(final_stmt)
            await session.commit()
            return res

    async def delete_by_id(self, id: UUID):
        async with async_session() as session:
            instance = await session.get(self.model, id)
            menu = (await session.execute(select(Menu).where(Submenu.menu_id == Menu.id))).scalars().first()
            await self.redis.delete(str(menu.id))
            await session.delete(instance)
            await session.commit()
            return 'delete success!'


class DishRepository(SQLAlchemyRepository):
    model = Dish

    async def add_one(self, data: dict) -> dict:
        async with async_session() as session:
            new_instance = self.model(**data)
            session.add(new_instance)
            await session.commit()
            submenu = (await session.execute(select(Submenu).where(new_instance.submenu_id == Submenu.id))).scalars().first()
            menu = (await session.execute(select(Menu).where(Submenu.menu_id == Menu.id))).scalars().first()
            await self.redis.delete(str(submenu.id))
            await self.redis.delete(str(menu.id))
            return new_instance

    async def update_by_id(self, id: UUID, data: dict) -> dict:
        async with async_session() as session:
            instance = await session.get(self.model, id)
            if data['title']:
                instance.title = data['title']
            if data['description']:
                instance.description = data['description']
            if data['price']:
                instance.price = data['price']
            await session.commit()
            await session.refresh(instance)
            return instance

    async def delete_by_id(self, id: UUID):
        async with async_session() as session:
            instance = await session.get(self.model, id)
            submenu = (await session.execute(select(Submenu).where(instance.submenu_id == Submenu.id))).scalars().first()
            menu = (await session.execute(select(Menu).where(Submenu.menu_id == Menu.id))).scalars().first()
            await self.redis.delete(str(submenu.id))
            await self.redis.delete(str(menu.id))
            await session.delete(instance)
            await session.commit()
            return 'delete success!'
