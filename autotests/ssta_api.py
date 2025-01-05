from autotests.controllers import UserAPI


class SSTAAPI:
    def __init__(self, base_url: str):
        self.user = UserAPI(base_url)
