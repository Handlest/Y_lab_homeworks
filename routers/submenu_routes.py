from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from config import get_db
from models.models import Dish, Menu, Submenu, Submenu_Pydantic
from utils import check_menu_and_submenu

submenu_router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus',
                           tags=['submenu'])


@submenu_router.get('')
async def get_submenu_list(target_menu_id: UUID, db: AsyncSession = Depends(get_db)):
    db_menu = await db.get(Menu, target_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    db_submenus = await db.execute(select(Submenu))
    return db_submenus.scalars().all()

# Пофиксить получение количества блюд


@submenu_router.get('/{target_submenu_id}')
async def get_submenu_by_id(target_menu_id: UUID, target_submenu_id: UUID, db: AsyncSession = Depends(get_db)):
    await check_menu_and_submenu(db, target_menu_id, target_submenu_id, status.HTTP_404_NOT_FOUND)
    db_submenu = await db.get(Submenu, target_submenu_id)
    dishes_count = await db.execute(select(func.count(Dish.id)).where(Dish.submenu_id == target_submenu_id))
    db_submenu.dishes_count = dishes_count.scalars().first()
    return db_submenu


@submenu_router.post('',
                     response_model=Submenu_Pydantic,
                     status_code=status.HTTP_201_CREATED)
async def create_submenu(submenu: Submenu_Pydantic, target_menu_id: UUID, db: AsyncSession = Depends(get_db)):
    db_menu = await db.get(Menu, target_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    new_submenu = Submenu(**submenu.dict())
    new_submenu.menu_id = target_menu_id
    db.add(new_submenu)
    await db.commit()
    await db.refresh(new_submenu)
    return new_submenu


@submenu_router.patch('/{target_submenu_id}',
                      response_model=Submenu_Pydantic)
async def update_submenu_by_id(new_submenu: Submenu_Pydantic, target_menu_id: UUID,
                               target_submenu_id: UUID, db: AsyncSession = Depends(get_db)):
    await check_menu_and_submenu(db, target_menu_id, target_submenu_id, status.HTTP_404_NOT_FOUND)
    db_submenu = await db.get(Submenu, target_submenu_id)
    if new_submenu.title:
        db_submenu.title = new_submenu.title
    if new_submenu.description:
        db_submenu.description = new_submenu.description
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


@submenu_router.delete('/{target_submenu_id}')
async def delete_submenu_by_id(target_menu_id: UUID, target_submenu_id: UUID, db: AsyncSession = Depends(get_db)):
    await check_menu_and_submenu(db, target_menu_id, target_submenu_id, status.HTTP_204_NO_CONTENT)
    db_submenu = await db.get(Submenu, target_submenu_id)
    await db.delete(db_submenu)
    await db.commit()
    return JSONResponse(content='Delete success!', status_code=status.HTTP_200_OK)
