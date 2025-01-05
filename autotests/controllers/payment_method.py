from service.schemas.payment_method import PaymentMethodCreate
from requests import Session, Response


class PaymentMethodAPI:
    def __init__(self, base_url: str):
        self.url = f'{base_url}/payment_method'

    def add_method(self, session: Session, data: PaymentMethodCreate) -> Response:
        return session.post(f'{self.url}/new', json=data.dict())

    def update_method(self, session: Session, method_id: int, data: PaymentMethodCreate) -> Response:
        return session.put(f'{self.url}/update/{method_id}', json=data.dict())

    def get_method_info(self, session: Session, method_id: int) -> Response:
        return session.get(f'{self.url}/info/{method_id}')

    def get_methods_list(self, session: Session) -> Response:
        return session.get(f'{self.url}/list')

    def delete_method(self, session: Session, method_id: int) -> Response:
        return session.delete(f'{self.url}/delete/{method_id}')
