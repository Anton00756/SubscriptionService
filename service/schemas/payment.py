from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    amount: float
    status: str
    open_date: datetime
    subscription_id: int

    class Config:
        from_attributes = True


class PaymentResponse(PaymentCreate):
    id: int

    class Config:
        from_attributes = True


class PaymentStatusUpdate(BaseModel):
    payment_id: int
    status: str
