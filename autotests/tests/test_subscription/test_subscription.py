import random
from uuid import uuid4

import allure
import pytest

from service.enums import SubscriptionRate
from service.schemas.subscription import SubscriptionCreate, SubscriptionResponse


@pytest.mark.parametrize('rate', list(SubscriptionRate))
def test_create_subscription(api, auth_session, rate):
    with allure.step('Оформляем подписку'):
        body = SubscriptionCreate(name=str(uuid4()), type=rate, price=100, duration=30)
        response = api.subscription.create_subscription(auth_session.session, body)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = SubscriptionResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.is_active
        result_data = response_data.dict()
        for key in ('id', 'is_active', 'open_date', 'end_date'):
            result_data.pop(key)
        assert result_data == body.dict()


@pytest.mark.parametrize('rate', list(SubscriptionRate))
def test_create_subscription_with_auto_renew(api, auth_session, rate, create_payment_method):
    with allure.step('Оформляем подписку'):
        body = SubscriptionCreate(
            name=str(uuid4()),
            type=rate,
            price=100,
            duration=30,
            payment_method_id=create_payment_method.id,
            auto_renew=True,
        )
        response = api.subscription.create_subscription(auth_session.session, body)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = SubscriptionResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data.is_active
        result_data = response_data.dict()
        for key in ('id', 'is_active', 'open_date', 'end_date'):
            result_data.pop(key)
        assert result_data == body.dict()


def test_get_subscription(api, auth_session, create_subscription):
    with allure.step('Получаем информацию о подписке'):
        response = api.subscription.get_subscription(auth_session.session, create_subscription.id)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = SubscriptionResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        assert response_data == create_subscription


def test_get_subscriptions_list(api, auth_session, create_subscription):
    with allure.step('Получаем информацию о подписках'):
        response = api.subscription.get_subscriptions_list(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        for subscription in response.json():
            SubscriptionResponse(**subscription)


def test_update_subscription(api, auth_session, create_subscription):
    with allure.step('Оформляем подписку'):
        body = SubscriptionCreate(name=str(uuid4()), type=random.choice(list(SubscriptionRate)), price=200, duration=60)
        response = api.subscription.update_subscription(auth_session.session, create_subscription.id, body)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        response_data = SubscriptionResponse(**response.json())

    with allure.step('Проверяем поля ответа'):
        request_data = body.dict()
        response_data = response_data.dict()
        for key, value in response_data.items():
            if key in request_data:
                assert value == request_data[key]
            else:
                assert value == getattr(create_subscription, key)


def test_cancel_subscription(api, auth_session, create_subscription):
    with allure.step('Отменяем подписку'):
        response = api.subscription.cancel_subscription(auth_session.session, create_subscription.id)
        assert response.status_code == 200

    with allure.step('Получаем информацию о подписке'):
        response = api.subscription.get_subscription(auth_session.session, create_subscription.id)
        assert response.status_code == 200

    with allure.step('Проверяем статус подписки'):
        response_data = SubscriptionResponse(**response.json())
        assert not response_data.is_active
