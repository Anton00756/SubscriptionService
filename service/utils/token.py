import os

from jose import JWTError, jwt
from datetime import datetime, timedelta


class TokenEngine:
    SECRET_KEY = os.environ.get('TOKEN_SECRET_KEY', '')
    ALGORITHM = 'HS256'

    @staticmethod
    def create_access_token(mail: str):
        data = {'mail': mail, 'exp': datetime.utcnow() + timedelta(minutes=60)}
        return jwt.encode(data, TokenEngine.SECRET_KEY, algorithm=TokenEngine.ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> tuple[bool, str]:
        try:
            payload = jwt.decode(token, TokenEngine.SECRET_KEY, algorithms=[TokenEngine.ALGORITHM])
            if payload['exp'] < datetime.utcnow().timestamp():
                return False, ''
            return True, payload['mail']
        except Exception:
            import traceback
            print(traceback.format_exc())
            return False, ''
