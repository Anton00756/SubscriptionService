from uuid import uuid4

import allure

from service.schemas.payment_method import PaymentMethodCreate, PaymentMethodResponse, ActivePaymentMethodResponse


def test_add_payment_method(api, auth_session):
    with allure.step('Добавляем новый метод оплаты'):
        body = PaymentMethodCreate(type='card', card_number=str(uuid4()), expiry_date='03/22', cvv=123)
        response = api.payment_method.add_method(auth_session.session, body)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = ActivePaymentMethodResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        result_data = response_data.dict()
        result_data.pop('id')
        assert result_data == body.dict()


def test_get_payment_method_info(api, auth_session, create_payment_method):
    with allure.step('Получаем информацию о методе оплаты'):
        response = api.payment_method.get_method_info(auth_session.session, create_payment_method.id)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = PaymentMethodResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.is_active
        result_data = response_data.dict()
        result_data.pop('is_active')
        assert result_data == create_payment_method.dict()


def test_get_payment_methods_list(api, auth_session, create_payment_method):
    with allure.step('Получаем список методов оплаты'):
        response = api.payment_method.get_methods_list(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        for method in response.json():
            ActivePaymentMethodResponse(**method)


def test_update_payment_method(api, auth_session, create_payment_method):
    with allure.step('Обновляем метод оплаты'):
        body = PaymentMethodCreate(type='paypal', card_number=str(uuid4()), expiry_date='03/24', cvv=567)
        response = api.payment_method.update_method(auth_session.session, create_payment_method.id, body)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = ActivePaymentMethodResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.id == create_payment_method.id
        result_data = response_data.dict()
        result_data.pop('id')
        assert result_data == body.dict()


def test_delete_payment_method(api, auth_session, create_payment_method):
    with allure.step('Удаляем метод оплаты'):
        response = api.payment_method.delete_method(auth_session.session, create_payment_method.id)
        assert response.status_code == 200

    with allure.step('Получаем список методов оплаты'):
        response = api.payment_method.get_methods_list(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем отсутствие метода в списке методов'):
        for method in response.json():
            assert create_payment_method.id != method['id']

    with allure.step('Получаем информацию о методе оплаты'):
        response = api.payment_method.get_method_info(auth_session.session, create_payment_method.id)
        assert response.status_code == 200

    with allure.step('Проверяем флаг is_active'):
        assert not PaymentMethodResponse(**response.json()).is_active
