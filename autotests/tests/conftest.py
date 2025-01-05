import os
import random
from dataclasses import dataclass
from uuid import uuid4

from pytest import fixture
from requests import Session

from autotests.ssta_api import SSTAAPI
from service.enums import SubscriptionRate
from service.schemas.payment import PaymentCreate, PaymentResponse
from service.schemas.payment_method import PaymentMethodCreate, ActivePaymentMethodResponse
from service.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from service.schemas.user import UserCreate
from service.utils import TokenEngine


@dataclass
class AuthSession:
    session: Session
    mail: str


@fixture(scope='session')
def api():
    return SSTAAPI(os.environ.get('SSTA_URL', ''))


@fixture
def auth_session(api):
    session = Session()
    random_mail = f'{uuid4()}@test.ru'
    response = api.user.register_user(session, UserCreate(email=random_mail, password=random_mail))
    assert response.status_code == 200
    yield AuthSession(session=session, mail=random_mail)


@fixture
def fake_user_session(api):
    session = Session()
    random_mail = f'{uuid4()}@test.ru'
    access_token = TokenEngine.create_access_token(random_mail)
    session.cookies.set('ssta_service', access_token)
    yield session


@fixture
def create_payment_method(api, auth_session):
    body = PaymentMethodCreate(type='card', card_number=str(uuid4()), expiry_date='03/22', cvv=123)
    response = api.payment_method.add_method(auth_session.session, body)
    assert response.status_code == 200
    yield ActivePaymentMethodResponse(**response.json())


@fixture
def create_subscription(api, auth_session):
    body = SubscriptionCreate(name=str(uuid4()), type=random.choice(list(SubscriptionRate)), price=100, duration=30)
    response = api.subscription.create_subscription(auth_session.session, body)
    assert response.status_code == 200
    yield SubscriptionResponse(**response.json())


@fixture
def create_payment(api, auth_session, create_payment_method, create_subscription):
    body = PaymentCreate(
        amount=create_subscription.price,
        subscription_id=create_subscription.id,
        payment_method_id=create_payment_method.id,
    )
    response = api.payment.create_payment(auth_session.session, body)
    assert response.status_code == 200
    yield PaymentResponse(**response.json())
