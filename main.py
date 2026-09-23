from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import engine, get_db, Base
from models import MenuItem

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cafe Menu API")

class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int
    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в меню нашего кафе!"}

@app.get("/menu", response_model=List[MenuItemResponse])
def get_menu(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()

@app.post("/menu", response_model=MenuItemResponse)
def add_menu_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    db_item = MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item