from service.schemas.subscription import SubscriptionCreate
from requests import Session, Response


class SubscriptionAPI:
    def __init__(self, base_url: str):
        self.url = f'{base_url}/subscription'

    def create_subscription(self, session: Session, data: SubscriptionCreate) -> Response:
        return session.post(f'{self.url}/new', json=data.dict())

    def get_subscription(self, session: Session, subscription_id: int) -> Response:
        return session.get(f'{self.url}/info/{subscription_id}')

    def get_subscriptions_list(self, session: Session) -> Response:
        return session.get(f'{self.url}/list')

    def update_subscription(self, session: Session, subscription_id: int, data: SubscriptionCreate) -> Response:
        return session.put(f'{self.url}/update/{subscription_id}', json=data.dict())

    def cancel_subscription(self, session: Session, subscription_id: int) -> Response:
        return session.delete(f'{self.url}/cancel/{subscription_id}')
