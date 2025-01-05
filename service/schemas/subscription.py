from datetime import datetime

from pydantic import BaseModel

from service.enums import SubscriptionRate


class SubscriptionCreate(BaseModel):
    name: str
    type: SubscriptionRate
    price: float
    is_active: bool = True
    auto_renew: bool = False
    open_date: datetime
    duration: int


class SubscriptionResponse(SubscriptionCreate):
    id: int
    end_date: datetime

    class Config:
        from_attributes = True
