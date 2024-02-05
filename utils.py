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


def reverse(route_name: str, **kwargs) -> str:
    routes = {
        'get_menu_list': '/api/v1/menus',
        'post_menu': '/api/v1/menus',
        'get_menu_by_id': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'patch_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'delete_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'get_submenu_list': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus',
        'post_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus',
        'get_submenu_by_id': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'patch_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'delete_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'get_dish_list': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}/dishes',
        'post_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}/dishes',
        'get_dish_by_id': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                          f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
        'patch_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                      f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
        'delete_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                       f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
    }
    return str(routes.get(route_name))
