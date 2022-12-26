import datetime

from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, password=user.password, registration_date=user.registration_date, id=user.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def find_user(db: Session, fname: str, lname: str):
    user = db.query(models.User).filter(models.User.first_name == fname).first() and db.query(models.User).filter(models.User.last_name == lname).first()
    return user

def change_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.password = user.password
    db_user.id = user.id
    db_user.registration_date = user.registration_date
    db.commit()
    db.refresh(db_user)
    return db_user