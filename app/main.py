import datetime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth


if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="🔥Brecht Voets 2CCS01's API🔥",description="Welcome to my cool user API, where I made a replica of what could become a login page that stores data in a database!")

origins = [
    "http://localhost:8000",
    "http://localhost",
    "https://brecht101.github.io"
    "https://jade-paletas-1d3f7e.netlify.app"
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
        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Try to authenticate the user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect mail or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.registration_date = datetime.datetime.now()
    return crud.create_user(db=db, user=user)

@app.post("/order")
def create_user(order: schemas.OderCreate, ownerID: int, warehouseID: int, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order, ownerID=ownerID, warehouseID=warehouseID)

@app.post("/warehouse")
def create_user(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return crud.create_warehouse(db=db, warehouse=warehouse)


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):#, token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/orders", response_model=list[schemas.Order])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):#, token: str = Depends(oauth2_scheme)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/warehouses", response_model=list[schemas.Warehouse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):#, token: str = Depends(oauth2_scheme)):
    warehouses = crud.get_warehouses(db, skip=skip, limit=limit)
    return warehouses

@app.get("/user", response_model=schemas.User)
def read_user(id: int = Query(default=None,gt=0,
                             description="This parameter needs the private ID of an account."), db: Session = Depends(get_db)):#, token: str = Depends(oauth2_scheme)):
    db_user = crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid ID")
    return db_user

@app.get("/id")
def read_id(fname: str, lname: str, db: Session = Depends(get_db)):#, token: str = Depends(oauth2_scheme)):
    user = crud.find_user(db, fname=fname, lname=lname)
    if user is None:
        raise HTTPException(status_code=404, detail="No user found!")
    return user.id
    
@app.put("/change")
def change_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):#, token: str = Depends(oauth2_scheme)):
    user.registration_date = datetime.datetime.now()
    db_user = crud.change_user(db, user_id=id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid ID!")
    return db_user

@app.delete("/remove")
def remove_user(id: int, db: Session = Depends(get_db)):#, token: str = Depends(oauth2_scheme)):
    db_user = crud.remove_user(db, user_id=id)
    return db_user