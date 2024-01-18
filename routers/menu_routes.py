from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from config import get_db
from models.menu import Menu_Pydantic, Menu

user_router = APIRouter()


@user_router.get("/api/v1/menus")
def get_menu_list(db: Session = Depends(get_db)):
    return db.query(Menu).all()


@user_router.get("/api/v1/menus/{target_menu_id}")
def get_menu_by_id(target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db.query(Menu).filter(Menu.id == target_menu_id).first()


@user_router.post("/api/v1/menus", response_model=Menu_Pydantic, status_code=status.HTTP_201_CREATED)
def create_menu(menu: Menu_Pydantic, db: Session = Depends(get_db)):
    new_menu = Menu(**menu.dict())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


@user_router.patch("/api/v1/menus/{target_menu_id}", response_model=Menu_Pydantic)
def update_menu_by_id(new_menu: Menu_Pydantic, target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_menu.title = new_menu.title
    db_menu.description = new_menu.description
    db.commit()
    db.refresh(db_menu)
    return db_menu


@user_router.delete("/api/v1/menus/{target_menu_id}")
def delete_menu_by_id(target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        return JSONResponse(content="", status_code=200)
    db.delete(db_menu)
    db.commit()
    return JSONResponse(content="", status_code=200)
