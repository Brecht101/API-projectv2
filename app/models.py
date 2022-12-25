from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class User(Base):
    __tablename__ = "data"

    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(50))
    registration_date = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True)
