from requests import Session, Response


class NotificationAPI:
    def __init__(self, base_url: str):
        self.url = f'{base_url}/notification'

    def get_notifications(self, session: Session) -> Response:
        return session.get(self.url)
