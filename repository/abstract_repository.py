from abc import ABC, abstractmethod
from typing import Any

import aioredis
from aioredis import Redis
from pydantic.types import UUID
from sqlalchemy import select

from config import async_session
from models.models import (
    CreateDishPydantic,
    CreateMenuPydantic,
    CreateSubmenuPydantic,
    Dish,
    Dish_Pydantic,
    Menu,
    Menu_Pydantic,
    Submenu,
    Submenu_Pydantic,
)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: CreateMenuPydantic | CreateSubmenuPydantic | CreateDishPydantic) -> Menu | Submenu | Dish:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_id(self, id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_title(self, title: str):
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, id: UUID, data: Menu_Pydantic | Submenu_Pydantic | Dish_Pydantic) -> Menu | Submenu | Dish:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, id: UUID):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    redis: Redis = aioredis.from_url('redis://redis/1')
    model: Any = None

    async def add_one(self, data: dict) -> Menu | Submenu | Dish:
        async with async_session() as session:
            new_instance = self.model(**data)
            session.add(new_instance)
            await session.commit()
            return new_instance

    async def find_one_by_id(self, id: UUID) -> Menu | Submenu | Dish:
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().first()

    async def find_one_by_title(self, title: str) -> Menu | Submenu | Dish:
        async with async_session() as session:
            stmt = select(self.model).where(self.model.title == title)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().first()

    async def find_all(self) -> list[Menu] | list[Submenu] | list[Dish]:
        async with async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().all()

    async def update_by_id(self, id: UUID, data: dict) -> Menu | Submenu | Dish:
        async with async_session() as session:
            instance = await session.get(self.model, id)
            if data['title']:
                instance.title = data['title']
            if data['description']:
                instance.description = data['description']
            await session.commit()
            await session.refresh(instance)
            return instance

    async def delete_by_id(self, id: UUID) -> str:
        async with async_session() as session:
            instance = await session.get(self.model, id)
            await session.delete(instance)
            await session.commit()
            return 'delete success!'
