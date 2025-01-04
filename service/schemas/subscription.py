from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    type: str
    is_active: bool = True


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
