from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def find_one_by_id(self):
        raise NotImplementedError
    @abstractmethod
    def find_all(self):
        raise NotImplementedError
    @abstractmethod
    def update_by_id(self):
        raise NotImplementedError
    @abstractmethod
    def delete_by_id(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    def find_one_by_id(self):
        pass

    def find_all(self):
        pass

    def update_by_id(self):
        pass

    def delete_by_id(self):
        pass