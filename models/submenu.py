import uuid

from sqlalchemy.dialects.postgresql import UUID
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, String
from config import Base


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
    description = Column(String)


Submenu_Pydantic = sqlalchemy_to_pydantic(Submenu)