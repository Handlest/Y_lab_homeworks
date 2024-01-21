import uuid
from re import match

from sqlalchemy.dialects.postgresql import UUID
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, validates

from config import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))

    @validates('price')
    def validate_price(self, _, value):
        pattern = r'^\d+(\.\d{1,2})?$'
        if match(pattern, value):
            return value
        else:
            raise ValueError('Неверный формат цены')


Dish_Pydantic = sqlalchemy_to_pydantic(Dish)


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    dish = relationship('Dish',  cascade='all, delete-orphan', backref="dishes")


Submenu_Pydantic = sqlalchemy_to_pydantic(Submenu)


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship('Submenu', cascade='all, delete-orphan', backref='submenus')


Menu_Pydantic = sqlalchemy_to_pydantic(Menu)














