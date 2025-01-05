from service.schemas.user import UserCreate, UserUpdate
from requests import Session, Response


class UserAPI:
    def __init__(self, base_url: str):
        self.url = f'{base_url}/user'

    def register_user(self, session: Session, data: UserCreate) -> Response:
        return session.post(f'{self.url}/register', json=data.dict())

    def login(self, session: Session, data: UserCreate) -> Response:
        return session.post(f'{self.url}/login', json=data.dict())

    def logout(self, session: Session) -> Response:
        return session.post(f'{self.url}/logout')

    def get_user_info(self, session: Session) -> Response:
        return session.get(f'{self.url}/info')

    def get_users_list(self, session: Session) -> Response:
        return session.get(f'{self.url}/list')

    def update_info(self, session: Session, data: UserUpdate) -> Response:
        return session.put(f'{self.url}/update', json=data.dict())

    def delete_user(self, session: Session) -> Response:
        return session.delete(f'{self.url}/delete')
