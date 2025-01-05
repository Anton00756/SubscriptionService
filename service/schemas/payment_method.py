from pydantic import BaseModel

class PaymentMethodCreate(BaseModel):
    type: str
    card_number: str
    expiry_date: str
    cvv: int


class PaymentMethodResponse(PaymentMethodCreate):
    id: int

    class Config:
        from_attributes = True


class PaymentMethodUpdate(BaseModel):
    type: str
    card_number: str
    expiry_date: str
    cvv: int
