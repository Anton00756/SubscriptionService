from uuid import uuid4

import allure
from requests import Session

from autotests.utils import get_random_str
from service.schemas.user import UserCreate, UserUpdate


def test_register_existing_user(api):
    session = Session()

    with allure.step('Регистрируем пользователя'):
        random_mail = f'{uuid4()}@test.ru'
        model = UserCreate(email=random_mail, password=random_mail)
        response = api.user.register_user(session, model)
        assert response.status_code == 200

    with allure.step('Регистрируем того же пользователя ещё раз'):
        response = api.user.register_user(session, model)
        assert response.status_code == 409


def test_login_nonexistent_user(api):
    session = Session()

    with allure.step('Авторизуемся'):
        random_mail = f'{uuid4()}@test.ru'
        response = api.user.login(session, UserCreate(email=random_mail, password=random_mail))
        assert response.status_code == 404


def test_login_user_with_bad_credentials(api):
    session = Session()

    with allure.step('Регистрируем пользователя'):
        random_mail = f'{uuid4()}@test.ru'
        response = api.user.register_user(Session(), UserCreate(email=random_mail, password=random_mail))
        assert response.status_code == 200

    with allure.step('Авторизуемся'):
        response = api.user.login(session, UserCreate(email=random_mail, password=get_random_str()))
        assert response.status_code == 401


def test_get_user_info_without_auth(api):
    with allure.step('Получаем информацию о пользователе'):
        response = api.user.get_user_info(Session())
        assert response.status_code == 401


def test_get_nonexistent_user_info(api, fake_user_session):
    with allure.step('Получаем информацию о пользователе'):
        response = api.user.get_user_info(fake_user_session)
        assert response.status_code == 404


def test_update_user_info_without_auth(api):
    with allure.step('Обновляем информацию о пользователе'):
        response = api.user.update_info(Session(), UserUpdate())
        assert response.status_code == 401


def test_update_nonexistent_user_info(api, fake_user_session):
    with allure.step('Обновляем информацию о пользователе'):
        response = api.user.update_info(fake_user_session, UserUpdate())
        assert response.status_code == 404


def test_delete_user_without_auth(api):
    with allure.step('Удаляем пользователя'):
        response = api.user.delete_user(Session())
        assert response.status_code == 401


def test_delete_nonexistent_user(api, fake_user_session):
    with allure.step('Удаляем пользователя'):
        response = api.user.delete_user(fake_user_session)
        assert response.status_code == 404
