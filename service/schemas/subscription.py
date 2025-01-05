from pydantic import BaseModel
from datetime import datetime

class SubscriptionCreate(BaseModel):
    name: str
    type: str
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
