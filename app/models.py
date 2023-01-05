from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "customers"

    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(50))
    email = Column(String, unique=True, index=True)
    registration_date = Column(DateTime)
    customerID = Column(Integer, primary_key=True, index=True)
    

class Order(Base):
    __tablename__ = "orders"
    
    orderID = Column(Integer, primary_key=True, index=True)
    orderItem =  Column(String)
    
    
    
class Storage(Base):
    __tablename__ = "warehouses"
    
    warehouseID = Column(Integer, primary_key=True, index=True)
    warehouseLocation = Column(String)
