from autotests.controllers import UserAPI, PaymentMethodAPI, SubscriptionAPI, PaymentAPI, NotificationAPI


class SSTAAPI:
    def __init__(self, base_url: str):
        self.user = UserAPI(base_url)
        self.payment_method = PaymentMethodAPI(base_url)
        self.subscription = SubscriptionAPI(base_url)
        self.payment = PaymentAPI(base_url)
        self.notification = NotificationAPI(base_url)
