from pydantic import BaseModel
from datetime import datetime


class PaymentBase(BaseModel):
    amount: float
    status: str
    open_date: datetime
    subscription_id: int

    class Config:
        from_attributes = True


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int

    class Config:
        orm_mode = True


class PaymentStatusUpdate(BaseModel):
    payment_id: int
    status: str
