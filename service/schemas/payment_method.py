from pydantic import BaseModel


class PaymentMethodBase(BaseModel):
    type: str
    details: str


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodResponse(PaymentMethodBase):
    id: int

    class Config:
        orm_mode = True


class PaymentMethodUpdate(BaseModel):
    type: str | None = None
    details: str | None = None
