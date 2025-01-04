from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from service.models import User
from service.schemas.user import UserCreate, UserResponse, UserUpdate
from service.database import get_db
from service.utils import PasswordEngine, TokenEngine
from fastapi import Response, Request

router = APIRouter()


@router.post(
    '/register',
    summary='Зарегистрировать пользователя',
    response_model=UserResponse,
    responses={409: {'description': 'Пользователь уже существует'}},
)
async def register_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    # Проверка, существует ли пользователь
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail='Пользователь уже существует')
    # Хеширование пароля
    hashed_password = PasswordEngine.hash_password(user.password)
    # Создание нового пользователя
    new_user = User(email=user.email, password=hashed_password, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = TokenEngine.create_access_token(user.email)
    response.set_cookie('ssta_service', access_token, httponly=True)
    return new_user


@router.post(
    '/login',
    summary='Авторизоваться в системе',
    responses={401: {}, 404: {'description': 'Пользователь не существует'}},
)
async def login_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    response.delete_cookie('ssta_service')
    if not existing_user:
        response.status_code = 404
        return response
    if not PasswordEngine.verify_password(user.password, existing_user.password):
        response.status_code = 401
        return response
    access_token = TokenEngine.create_access_token(user.email)
    response.set_cookie('ssta_service', access_token, httponly=True)
    response.status_code = 200
    return response


@router.post(
    '/logout',
    summary='Выйти из системы',
    response_class=Response
)
async def logout(response: Response):
    response.delete_cookie('ssta_service')
    return Response(status_code=200)


@router.get(
    '/info',
    summary='Получить информацию о текущем пользователе',
    response_model=UserResponse,
    responses={401: {}, 404: {'description': 'Пользователь не существует'}},
)
async def get_user_info(request: Request, db: Session = Depends(get_db)):
    if not (cookie_result := TokenEngine.verify_token(request.cookies.get('ssta_service')))[0]:
        raise HTTPException(status_code=401)
    user = db.query(User).filter(User.email == cookie_result[1]).first()
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.get('/list', summary='Получить список зарегистрированных пользователей', response_model=list[UserResponse])
async def get_user_list(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.put(
    '/update',
    summary='Обновить информацию о текущем пользователе',
    response_model=UserResponse,
    responses={401: {}, 404: {'description': 'Пользователь не существует'}},
)
async def update_user(response: Response, user_update: UserUpdate, request: Request, db: Session = Depends(get_db)):
    if not (cookie_result := TokenEngine.verify_token(request.cookies.get('ssta_service')))[0]:
        raise HTTPException(status_code=401)
    user = db.query(User).filter(User.email == cookie_result[1]).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не существует')

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    access_token = TokenEngine.create_access_token(user.email)
    response.set_cookie('ssta_service', access_token, httponly=True)
    return user


@router.delete(
    '/delete',
    summary='Удалить текущего пользователя',
    response_class=Response,
    responses={401: {}, 404: {'description': 'Пользователь не существует'}},
)
async def delete_user(request: Request, db: Session = Depends(get_db)):
    if not (cookie_result := TokenEngine.verify_token(request.cookies.get('ssta_service')))[0]:
        return Response(status_code=401)
    user = db.query(User).filter(User.email == cookie_result[1]).first()
    if not user:
        return Response(status_code=404)
    db.delete(user)
    db.commit()
    response = Response(status_code=200)
    response.delete_cookie('ssta_service')
    return response
