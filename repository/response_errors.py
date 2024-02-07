from pydantic import BaseModel


class ResponseAlreadyTakenError(BaseModel):
    detail: str = 'The title has already been taken'


class ResponseDishNotFoundError(BaseModel):
    detail: str = 'dish not found'


class ResponseMenuNotFoundError(BaseModel):
    detail: str = 'menu not found'


class ResponseSubmenuNotFoundError(BaseModel):
    detail: str = 'submenu not found'
