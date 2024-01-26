from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from config import get_db
from models import Menu_Pydantic, Menu, Submenu, Dish

menu_router = APIRouter(prefix="/api/v1/menus", tags=["menu"])


@menu_router.get("/")
def get_menu_list(db: Session = Depends(get_db)):
    menu_list = db.query(Menu).all()
    return menu_list


@menu_router.get("/{target_menu_id}")
def get_menu_by_id(target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    submenus_count_query = (db.query(func.count(Submenu.id))
                            .filter(Submenu.menu_id == target_menu_id)
                            .subquery())

    dishes_count_query = (db.query(func.count(Dish.id))
                          .join(Submenu)
                          .filter(Submenu.menu_id == target_menu_id)
                          .subquery())

    # Объединение двух подзапросов в один
    combined_query = (db.query(submenus_count_query, dishes_count_query)
                      .union(db.query(dishes_count_query, submenus_count_query))
                      .first())

    submenus_count, dishes_count = combined_query
    db_menu.submenus_count = submenus_count
    db_menu.dishes_count = dishes_count

    return db_menu


@menu_router.post("/", response_model=Menu_Pydantic, status_code=status.HTTP_201_CREATED)
def create_menu(menu: Menu_Pydantic, db: Session = Depends(get_db)):
    new_menu = Menu(**menu.dict())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


@menu_router.patch("/{target_menu_id}", response_model=Menu_Pydantic)
def update_menu_by_id(new_menu: Menu_Pydantic, target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db_menu.title = new_menu.title
    db_menu.description = new_menu.description
    db.commit()
    db.refresh(db_menu)
    return db_menu


@menu_router.delete("/{target_menu_id}")
def delete_menu_by_id(target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        return JSONResponse(content="Not found", status_code=status.HTTP_204_NO_CONTENT)
    db.delete(db_menu)
    db.commit()
    return JSONResponse(content="Delete success!", status_code=status.HTTP_200_OK)
