from repository.abstract_repository import AbstractRepository


class AppService:
    def __init__(self, repository: AbstractRepository):
        self._repository: AbstractRepository = repository
    # some tasks in future
