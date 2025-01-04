from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: float
    status: str


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int

    class Config:
        orm_mode = True


class PaymentStatusUpdate(BaseModel):
    payment_id: int
    status: str
