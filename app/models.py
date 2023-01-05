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
    
    order = relationship("Order", back_populates="customer")
    warehouse = relationship("Storage", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    
    orderID = Column(Integer, primary_key=True, index=True)
    orderItem =  Column(String)
    ownerID = Column(Integer, ForeignKey("customers.customerID"))
    warehouseID = Column(Integer, ForeignKey("warehouses.warehouseID"))
    
    customer = relationship("User", back_populates="order")
    warehouse = relationship("Storage", back_populates="order")
    
    
class Storage(Base):
    __tablename__ = "warehouses"
    
    warehouseID = Column(Integer, primary_key=True, index=True)
    warehouseLocation = Column(String)
    
    oder = relationship("Order", back_populates="warehouse")