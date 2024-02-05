import uuid
from re import match

from pydantic import BaseModel
from pydantic.types import UUID4
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from config import Base


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))

    @validates('price')
    def validate_price(self, _, value: str):
        pattern = r'^\d+(\.\d{1,2})?$'
        if match(pattern, value):
            return value
        else:
            raise ValueError('Неверный формат цены')

    def as_dict(self) -> dict:
        dictionary = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dictionary['id'] = str(dictionary['id'])
        dictionary['submenu_id'] = str(dictionary['submenu_id'])
        return dictionary


Dish_Pydantic = sqlalchemy_to_pydantic(Dish)


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    dish = relationship('Dish', cascade='all, delete-orphan', backref='dishes')

    def as_dict(self) -> dict:
        dictionary = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dictionary['id'] = str(dictionary['id'])
        dictionary['menu_id'] = str(dictionary['menu_id'])
        return dictionary


Submenu_Pydantic = sqlalchemy_to_pydantic(Submenu)


class FullSubmenuPydantic(BaseModel):
    id: UUID4
    title: str
    description: str
    menu_id: UUID4
    dishes_count: int

    class Config:
        orm_mode = True


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship('Submenu', cascade='all, delete-orphan', backref='submenus')

    def as_dict(self) -> dict:
        dictionary = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dictionary['id'] = str(dictionary['id'])
        return dictionary


Menu_Pydantic = sqlalchemy_to_pydantic(Menu)


class FullMenuPydantic(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus: UUID4 | None
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
