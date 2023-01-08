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
    
    orders = relationship("Order", back_populates="customer")
    

class Order(Base):
    __tablename__ = "orders"
    
    orderID = Column(Integer, primary_key=True, index=True)
    orderItem =  Column(String)
    customerID = Column(Integer, ForeignKey("customers.customerID"))
    warehouseID = Column(Integer, ForeignKey("warehouses.warehouseID"))
    
    customer = relationship("User", back_populates="orders")
    warehouse = relationship("Storage", back_populates="orders")
    
    
    
class Storage(Base):
    __tablename__ = "warehouses"
    
    warehouseID = Column(Integer, primary_key=True, index=True)
    warehouseLocation = Column(String)
    
    orders = relationship("Order", back_populates="warehouse")
