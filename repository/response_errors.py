from pydantic import BaseModel


class ResponseAlreadyTakenError(BaseModel):
    response: str = 'The title has already been taken'


class ResponseNotFoundError(BaseModel):
    response: str = 'Requested object with given id was not found'
