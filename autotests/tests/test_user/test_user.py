from uuid import uuid4

import allure
from requests import Session

from service.schemas.user import UserCreate, UserUpdate, UserResponse


def test_register_user(api):
    session = Session()

    with allure.step('Регистрируем пользователя'):
        random_mail = f'{uuid4()}@test.ru'
        response = api.user.register_user(session, UserCreate(email=random_mail, password=random_mail))
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = UserResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.email == random_mail and response_data.is_active

    with allure.step('Проверяем, что проставилась кука авторизации'):
        assert session.cookies.get('ssta_service')


def test_login_user(api):
    session = Session()

    with allure.step('Регистрируем пользователя'):
        random_mail = f'{uuid4()}@test.ru'
        response = api.user.register_user(Session(), UserCreate(email=random_mail, password=random_mail))
        assert response.status_code == 200

    with allure.step('Авторизуемся'):
        response = api.user.login(session, UserCreate(email=random_mail, password=random_mail))
        assert response.status_code == 200

    with allure.step('Проверяем, что проставилась кука авторизации'):
        assert response.cookies.get('ssta_service')


def test_logout_user(api, auth_session):
    with allure.step('Выходим из системы'):
        response = api.user.logout(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем, что кука авторизации удалена'):
        assert not auth_session.session.cookies.get('ssta_service')


def test_get_user_info(api, auth_session):
    with allure.step('Получаем информацию о пользователе'):
        response = api.user.get_user_info(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = UserResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.email == auth_session.mail


def test_get_users_list(api):
    with allure.step('Получаем список зарегистрированных пользователей'):
        response = api.user.get_users_list(Session())
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        for user in response.json():
            UserResponse(**user)


def test_update_user_info(api, auth_session):
    with allure.step('Получаем информацию о пользователе'):
        response = api.user.get_user_info(auth_session.session)
        assert response.status_code == 200
        user_id = UserResponse(**response.json()).id

    with allure.step('Обновляем информацию о пользователе'):
        random_mail = f'{uuid4()}@test.ru'
        response = api.user.update_info(auth_session.session, UserUpdate(email=random_mail, is_active=False))
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = UserResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.email == random_mail and response_data.id == user_id and not response_data.is_active

    with allure.step('Проверяем, что обновилась информация о пользователе'):
        response = api.user.get_user_info(auth_session.session)
        assert response.status_code == 200
        response_data = UserResponse(**response.json())
        assert response_data.email == random_mail and response_data.id == user_id and not response_data.is_active


def test_delete_user(api, auth_session):
    with allure.step('Удаляем пользователя'):
        response = api.user.delete_user(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем, что кука авторизации удалена'):
        assert not auth_session.session.cookies.get('ssta_service')

    with allure.step('Проверяем, что пользователь удален'):
        response = api.user.login(auth_session.session, UserCreate(email=auth_session.mail, password=auth_session.mail))
        assert response.status_code == 404
