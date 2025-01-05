import allure
import pytest

from service.enums import PaymentStatus
from service.schemas.payment import PaymentCreate, PaymentResponse, PaymentStatusUpdate


def test_create_payment(api, auth_session, create_payment_method, create_subscription):
    with allure.step('Создаём платёж'):
        body = PaymentCreate(
            amount=create_subscription.price,
            subscription_id=create_subscription.id,
            payment_method_id=create_payment_method.id,
        )
        response = api.payment.create_payment(auth_session.session, body)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = PaymentResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.status == PaymentStatus.CREATED
        result_data = response_data.dict()
        for key in ('id', 'status', 'open_date'):
            result_data.pop(key)
        assert result_data == body.dict()


def test_get_payments(api, auth_session, create_payment):
    with allure.step('Получаем список платежей'):
        response = api.payment.get_payments_list(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        for payment in response.json():
            PaymentResponse(**payment)


@pytest.mark.parametrize('status', list(PaymentStatus))
def test_set_payment_status(api, auth_session, create_payment, status):
    with allure.step('Устанавливаем статус платежа'):
        body = PaymentStatusUpdate(payment_id=create_payment.id, status=status)
        response = api.payment.set_payment_status(auth_session.session, body)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = PaymentResponse(**response.json())

    with allure.step('Проверяем статус платежа'):
        assert response_data.id == create_payment.id and response_data.status == status
