from fastapi import HTTPException
from pydantic.types import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.models import Menu, Submenu


async def check_menu_and_submenu(db: AsyncSession, menu_id: UUID, submenu_id: UUID,
                                 status_code_to_return: status.HTTP_404_NOT_FOUND):
    db_menu = await db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status_code_to_return, detail='menu not found')
    db_submenu = await db.get(Submenu, submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=status_code_to_return, detail='submenu not found')


def validate_price(price: str):
    return len(price.split('.')[-1]) in (1, 2)


def create_menu_json():
    data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    return data


def create_submenu_json():
    data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    return data


def create_dish_json(number: int = 1):
    if number == 1:
        data = {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50'
        }
    else:
        data = {
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50'
        }
    return data


async def create_menu(db: AsyncSession):
    menu = create_menu_json()
    new_menu = Menu(**menu)
    db.add(new_menu)
    await db.commit()
    return str(new_menu.id)


async def create_submenu(db: AsyncSession):
    menu_id = await create_menu(db)
    submenu = create_submenu_json()
    submenu['menu_id'] = menu_id
    new_submenu = Submenu(**submenu)
    db.add(new_submenu)
    await db.commit()
    return menu_id, str(new_submenu.id)
