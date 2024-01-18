import uuid
from sqlalchemy.dialects.postgresql import UUID
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, String
from config import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
    description = Column(String)


Menu_Pydantic = sqlalchemy_to_pydantic(Menu)
