from service.schemas.payment import PaymentCreate, PaymentStatusUpdate
from requests import Session, Response


class PaymentAPI:
    def __init__(self, base_url: str):
        self.url = f'{base_url}/payment'

    def create_payment(self, session: Session, data: PaymentCreate) -> Response:
        return session.post(f'{self.url}/new', json=data.dict())

    def get_payments_list(self, session: Session) -> Response:
        return session.get(f'{self.url}/list')

    def set_payment_status(self, session: Session, data: PaymentStatusUpdate) -> Response:
        return session.post(f'{self.url}/set_status', json=data.dict())
