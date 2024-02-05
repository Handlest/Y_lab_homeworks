from abc import ABC, abstractmethod
from typing import Any

import aioredis
from aioredis import Redis
from pydantic.types import UUID
from sqlalchemy import select

from config import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_id(self, id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, id: UUID, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, id: UUID):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    redis: Redis = aioredis.from_url('redis://redis/1')
    model: Any = None

    async def add_one(self, data: dict) -> dict:
        async with async_session() as session:
            new_instance = self.model(**data)
            session.add(new_instance)
            await session.commit()
            return new_instance

    async def find_one_by_id(self, id: UUID):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().first()

    async def find_all(self):
        async with async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().all()

    async def update_by_id(self, id: UUID, data: dict) -> dict:
        async with async_session() as session:
            instance = await session.get(self.model, id)
            if data['title']:
                instance.title = data['title']
            if data['description']:
                instance.description = data['description']
            await session.commit()
            await session.refresh(instance)
            return instance

    async def delete_by_id(self, id: UUID):
        async with async_session() as session:
            instance = await session.get(self.model, id)
            await session.delete(instance)
            await session.commit()
            return 'delete success!'
