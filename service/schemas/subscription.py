from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    name: str
    type: str
    price: float
    is_active: bool = True
    auto_renew: bool = False
    duration: int


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
