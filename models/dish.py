import uuid
from sqlalchemy.dialects.postgresql import UUID
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, String, Float
from config import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)


Dish_Pydantic = sqlalchemy_to_pydantic(Dish)