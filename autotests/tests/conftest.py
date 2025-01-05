import os
from dataclasses import dataclass
from uuid import uuid4

from pytest import fixture
from requests import Session

from autotests.ssta_api import SSTAAPI
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
