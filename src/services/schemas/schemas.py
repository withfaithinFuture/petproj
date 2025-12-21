import datetime
from typing import List
from pydantic import Field, BaseModel
from uuid import UUID
from decimal import Decimal

letters = r'^[A-Za-zА-Яа-яЁё\s]+$'

#клуб + футболисты (многие ко многим)
class ClubSchema(BaseModel):
    name: str = Field(min_length=3,  pattern=letters)
    home_town: str = Field(min_length=3,  pattern=letters)
    creation_date: datetime.date
    players: List["PlayerSchema"]

    class Config:
        from_attributes = True #принятие не только словарей но и других объектов с аттр

class PlayerSchema(BaseModel):
    first_name: str = Field(min_length=3, pattern=letters)
    last_name: str = Field(min_length=3, pattern=letters)
    played_in_club: datetime.date

    class Config:
        from_attributes = True

#биржа + владелец (1 к 1)
class ExchangeOwnerSchema(BaseModel):
    first_name: str = Field(min_length=3, pattern=letters)
    last_name: str = Field(min_length=3, pattern=letters)


class ExchangeSchema(BaseModel):
    owner: ExchangeOwnerSchema
    name: str = Field(min_length=3, pattern=letters)
    work_in_Russia: bool
    volume: float


#юзеры и акции (1 к многие)
class UserSchema(BaseModel):
    username: str = Field(min_length=3, pattern=letters)
    shares: List["SharesSchema"]

class SharesSchema(BaseModel):
    ticker: str = Field(min_length=2, pattern=letters)
    quantity: float
    purchase_price: Decimal
    purchase_date: datetime.date