from pydantic import BaseModel
from datetime import datetime
from service.enums import PaymentStatus


class PaymentCreate(BaseModel):
    amount: float
    open_date: datetime
    subscription_id: int
    payment_method_id: int


class PaymentResponse(PaymentCreate):
    id: int
    status: PaymentStatus

    class Config:
        from_attributes = True


class PaymentStatusUpdate(BaseModel):
    payment_id: int
    status: PaymentStatus
