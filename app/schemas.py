from datetime import datetime

from pydantic import BaseModel


class OrderBase(BaseModel):
    orderItem: str
    
class OderCreate(OrderBase):
    pass

class Order(OrderBase):
    orderID: int
    customerID: int
    warehouseID: int
    
    class Config:
        orm_mode = True
        
class WarehouseBase(BaseModel):
    warehouseLocation: str

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    warehouseID: int
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    registration_date: datetime | None = None


class UserCreate(UserBase):
    password: str

class User(UserBase):
    customerID: int
    orders: list[Order] = []
    
    class Config:
        orm_mode = True