from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    registration_date: datetime | None = None
    id: int | None = None


class UserCreate(UserBase):
    password: str

class User(UserBase):

    class Config:
        orm_mode = True