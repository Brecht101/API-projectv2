import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException


import models
import schemas
import auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.customerID == user_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_warehouses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Storage).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, password=hashed_password, email=user.email, registration_date=user.registration_date)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_order(db: Session, order: schemas.OderCreate, customerID: int, warehouseID: int):
    if db.query(models.User).filter(models.User.customerID == customerID).first() is None:
        return "Invalid user"
    if db.query(models.Storage).filter(models.Storage.warehouseID == warehouseID).first() is None:
        return "Invalid warehouse"
    db_order =  models.Order(**order.dict(), customerID=customerID, warehouseID=warehouseID)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    db_warehouse = models.Storage(warehouseLocation = warehouse.warehouseLocation)
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def change_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.customerID == user_id).first()
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.password = auth.get_password_hash(user.password)
    db_user.registration_date = user.registration_date
    db.commit()
    db.refresh(db_user)
    return db_user

def remove_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.customerID == user_id).first()
    orders = db.query(models.Order).filter(models.Order.customerID == user_id).all()
    for item in orders:
        db.delete(item)
    db.delete(db_user)
    db.commit()
    return db_user
    