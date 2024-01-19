from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from config import get_db
from models import Menu, Submenu, Submenu_Pydantic, Dish

submenu_router = APIRouter()


@submenu_router.get("/api/v1/menus/{target_menu_id}/submenus")
def get_submenu_list(target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db.query(Submenu).filter(Submenu.menu_id == target_menu_id).all()


@submenu_router.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
def get_submenu_by_id(target_menu_id: UUID, target_submenu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db_submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id and Submenu.menu_id == target_menu_id).first()
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    dishes_count = db.query(Dish).join(Submenu).filter(Submenu.menu_id == target_menu_id).count()
    db_submenu.dishes_count = dishes_count
    return db_submenu


@submenu_router.post("/api/v1/menus/{target_menu_id}/submenus",
                     response_model=Submenu_Pydantic,
                     status_code=status.HTTP_201_CREATED)
def create_submenu(submenu: Submenu_Pydantic, target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    new_submenu = Submenu(**submenu.dict())
    new_submenu.menu_id = target_menu_id
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


@submenu_router.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}",
                      response_model=Submenu_Pydantic)
def update_submenu_by_id(new_submenu: Submenu_Pydantic, target_menu_id: UUID,
                         target_submenu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id).first()
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    db_submenu.title = new_submenu.title
    db_submenu.description = new_submenu.description
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


@submenu_router.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
def delete_menu_by_id(target_menu_id: UUID, target_submenu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        return JSONResponse(content="", status_code=200)
    db_submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id).first()
    if db_submenu is None:
        return JSONResponse(content="", status_code=200)
    db.delete(db_submenu)
    db.commit()
    return JSONResponse(content="", status_code=200)
