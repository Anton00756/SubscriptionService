import allure

from service.schemas.notification import NotificationResponse


def test_get_notifications(api, auth_session, create_payment):
    with allure.step('Добавляем новый метод оплаты'):
        response = api.notification.get_notifications(auth_session.session)
        assert response.status_code == 200

    with allure.step('Проверяем схему ответа'):
        for notification in response.json():
            NotificationResponse(**notification)
