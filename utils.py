from fastapi import HTTPException
from pydantic.types import UUID
from sqlalchemy.orm import Session
from starlette import status
from models import Menu, Submenu


def check_menu_and_submenu(db: Session, menu_id: UUID, submenu_id: UUID,
                           status_code_to_return: status.HTTP_404_NOT_FOUND):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=status_code_to_return, detail="menu not found")
    db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if db_submenu is None:
        raise HTTPException(status_code=status_code_to_return, detail="submenu not found")


def validate_price(price: str):
    return len(price.split(".")[-1]) in (1, 2)