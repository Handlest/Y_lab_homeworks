from pydantic import BaseModel


class ResponseAlreadyTakenError(BaseModel):
    response: str = 'The title is already taken'


class ResponseNotFoundError(BaseModel):
    response: str = 'Not found'
