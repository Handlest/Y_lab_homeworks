from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy import func, select
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from config import get_db
from models.models import Dish, Menu, Menu_Pydantic, Submenu

menu_router = APIRouter(prefix='/api/v1/menus', tags=['menu'])


@menu_router.get('')
async def get_menu_list(db: AsyncSession = Depends(get_db)):
    menu_list: ChunkedIteratorResult = await db.execute(select(Menu))
    return menu_list.scalars().all()


@menu_router.get('/{target_menu_id}')
async def get_menu_by_id(target_menu_id: UUID, db: AsyncSession = Depends(get_db)):
    db_menu: ChunkedIteratorResult = await db.get(Menu, target_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')

    dishes_stmt = select(func.count(Dish.id)).join(Submenu).where(Submenu.menu_id == target_menu_id).scalar_subquery()

    submenus_stmt = select(func.count(Submenu.id)).where(Submenu.menu_id == target_menu_id).scalar_subquery()

    # Объединение двух подзапросов в один
    combined_query = await db.execute(select(Menu, submenus_stmt, dishes_stmt).where(Menu.id == target_menu_id))

    result = combined_query.fetchall()

    db_menu.submenus_count = result[0][1]
    db_menu.dishes_count = result[0][2]
    return db_menu


@menu_router.post('', response_model=Menu_Pydantic, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: Menu_Pydantic, db: AsyncSession = Depends(get_db)):
    new_menu = Menu(**menu.dict())
    db.add(new_menu)
    await db.commit()
    return new_menu


@menu_router.patch('/{target_menu_id}', response_model=Menu_Pydantic)
async def update_menu_by_id(new_menu: Menu_Pydantic, target_menu_id: UUID, db: AsyncSession = Depends(get_db)):
    db_menu = await db.get(Menu, target_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if new_menu.title:
        db_menu.title = new_menu.title
    if new_menu.description:
        db_menu.description = new_menu.description
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@menu_router.delete('/{target_menu_id}')
async def delete_menu_by_id(target_menu_id: UUID, db: AsyncSession = Depends(get_db)):
    db_menu = await db.get(Menu, target_menu_id)
    if db_menu is None:
        return JSONResponse(content='Not found', status_code=status.HTTP_204_NO_CONTENT)
    await db.delete(db_menu)
    await db.commit()
    return JSONResponse(content='Delete success!', status_code=status.HTTP_200_OK)
