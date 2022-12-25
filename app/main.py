import datetime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="🔥Brecht Voets 2CCS01's API🔥",description="Welcome to my cool user API, where I made a replica of what could become a login page that stores data in a database!")

origins = [
    "http://localhost:8000",
    "http://localhost",
    "https://brecht101.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/create")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.registration_date = datetime.datetime.now()
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/user", response_model=schemas.User)
def read_user(id: int = Query(default=None,gt=0,
                             description="This parameter needs the private ID of an account."), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid ID")
    return db_user
