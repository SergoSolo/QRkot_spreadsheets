from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "full_amount": 1000,
                "comment": "На нужды котиков"
            }
        }


class DonationUserDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationUserDB):
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
