from fastapi import HTTPException
from fastapi import Request, Response

from service.utils import TokenEngine


def get_user_from_cookie(request: Request):
    if not (cookie_result := TokenEngine.verify_token(request.cookies.get('ssta_service')))[0]:
        raise HTTPException(status_code=401)
    yield cookie_result[1]


def set_user_in_cookie(response: Response, user: str):
    access_token = TokenEngine.create_access_token(user)
    response.set_cookie('ssta_service', access_token, httponly=True)


def reset_user_from_cookie(response: Response):
    response.delete_cookie('ssta_service')
