from abc import ABC, abstractmethod

from sqlalchemy import insert

from config import get_db


class AbstractRepository(ABC):
    @abstractmethod
    async def find_one_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def find_one_by_id(self):
        async with get_db() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self):
        pass

    async def update_by_id(self):
        pass

    async def delete_by_id(self):
        pass
