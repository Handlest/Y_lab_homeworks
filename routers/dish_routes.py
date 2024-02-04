from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from config import get_db
from models.models import Dish, Dish_Pydantic
from utils import check_menu_and_submenu, validate_price

dish_router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=['dish'])


@dish_router.get('')
async def get_dishes_list(target_submenu_id: UUID, db: AsyncSession = Depends(get_db)):
    # Убрал проверку наличия меню и подменю, т.к. один из тестов требует возвращать пустой ответ даже если
    # подменю не существует
    dish_list: ChunkedIteratorResult = await db.execute(select(Dish))
    return dish_list.scalars().all()


@dish_router.get('/{target_dish_id}')
async def get_dish_by_id(target_menu_id: UUID, target_submenu_id: UUID, target_dish_id: UUID, db: AsyncSession = Depends(get_db)):
    await check_menu_and_submenu(db, target_menu_id, target_submenu_id, status.HTTP_404_NOT_FOUND)
    db_dish = await db.get(Dish, target_dish_id)
    if db_dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    return db_dish


@dish_router.post('', response_model=Dish_Pydantic,
                  status_code=status.HTTP_201_CREATED)
async def create_dish(dish: Dish_Pydantic, target_menu_id: UUID, target_submenu_id: UUID, db: AsyncSession = Depends(get_db)):
    await check_menu_and_submenu(db, target_menu_id, target_submenu_id, status.HTTP_404_NOT_FOUND)
    if not validate_price(dish.price):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='price is not valid')
    new_dish = Dish(**dish.dict())
    new_dish.menu_id = target_menu_id
    new_dish.submenu_id = target_submenu_id
    db.add(new_dish)
    await db.commit()
    await db.refresh(new_dish)
    return new_dish


@dish_router.patch('/{target_dish_id}',
                   response_model=Dish_Pydantic)
async def update_dish_by_id(new_dish: Dish_Pydantic, target_menu_id: UUID,
                            target_submenu_id: UUID, target_dish_id: UUID, db: AsyncSession = Depends(get_db)):
    await check_menu_and_submenu(db, target_menu_id, target_submenu_id, status.HTTP_404_NOT_FOUND)
    if new_dish.price is not None and not validate_price(new_dish.price):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='price is not valid')
    db_dish = await db.get(Dish, target_dish_id)
    if db_dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    if new_dish.title:
        db_dish.title = new_dish.title
    if new_dish.description:
        db_dish.description = new_dish.description
    if new_dish.price:
        db_dish.price = new_dish.price
    await db.commit()
    await db.refresh(db_dish)
    return db_dish


@dish_router.delete('/{target_dish_id}')
async def delete_dish_by_id(target_menu_id: UUID, target_submenu_id: UUID, target_dish_id: UUID,
                            db: AsyncSession = Depends(get_db)):
    await check_menu_and_submenu(db, target_menu_id, target_submenu_id, status.HTTP_204_NO_CONTENT)
    db_dish = await db.get(Dish, target_dish_id)
    await db.delete(db_dish)
    await db.commit()
    return JSONResponse(content='Delete success!', status_code=status.HTTP_200_OK)
