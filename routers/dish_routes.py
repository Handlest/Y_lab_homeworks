from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from config import get_db
from models import Menu, Submenu, Dish, Dish_Pydantic

dish_router = APIRouter()


def check_menu_and_submenu(db: Session, menu_id: UUID, submenu_id: UUID):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")


@dish_router.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes")
def get_dishes_list(target_menu_id: UUID, target_submenu_id: UUID, db: Session = Depends(get_db)):
    return db.query(Dish).filter(Dish.submenu_id == target_submenu_id).all()


@dish_router.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def get_dish_by_id(target_menu_id: UUID, target_submenu_id: UUID, target_dish_id: UUID, db: Session = Depends(get_db)):
    check_menu_and_submenu(db, target_menu_id, target_submenu_id)
    db_dish = db.query(Dish).filter(Dish.id == target_dish_id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@dish_router.post("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
                     response_model=Dish_Pydantic,
                     status_code=status.HTTP_201_CREATED)
def create_dish(dish: Dish_Pydantic, target_menu_id: UUID, target_submenu_id: UUID, db: Session = Depends(get_db)):
    check_menu_and_submenu(db, target_menu_id, target_submenu_id)
    new_dish = Dish(**dish.dict())
    new_dish.menu_id = target_menu_id
    new_dish.submenu_id = target_submenu_id
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


@dish_router.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
                      response_model=Dish_Pydantic)
def update_dish_by_id(new_dish: Dish_Pydantic, target_menu_id: UUID,
                         target_submenu_id: UUID, target_dish_id: UUID, db: Session = Depends(get_db)):
    check_menu_and_submenu(db, target_menu_id, target_submenu_id)
    db_dish = db.query(Dish).filter(Dish.id == target_dish_id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    db_dish.title = new_dish.title
    db_dish.description = new_dish.description
    db_dish.price = new_dish.price
    db.commit()
    db.refresh(db_dish)
    return db_dish


@dish_router.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def delete_menu_by_id(target_menu_id: UUID, target_submenu_id: UUID, target_dish_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        return JSONResponse(content="", status_code=200)
    db_submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id).first()
    if db_submenu is None:
        return JSONResponse(content="", status_code=200)
    db_dish = db.query(Dish).filter(Dish.id == target_dish_id).first()
    db.delete(db_dish)
    db.commit()
    return JSONResponse(content="", status_code=200)