from pydantic import BaseModel


class PaymentMethodBase(BaseModel):
    type: str
    card_number: str
    expiry_date: str
    cvv: int


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodResponse(PaymentMethodBase):
    id: int

    class Config:
        orm_mode = True


class PaymentMethodUpdate(BaseModel):
    type: str
    card_number: str
    expiry_date: str
    cvv: int
