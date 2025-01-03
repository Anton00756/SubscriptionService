from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from db.database import get_db
from utils.password import hash_password

router = APIRouter()


@router.post(
    "/register",
    summary="Зарегистрировать пользователя",
    response_model=UserResponse
)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка, существует ли пользователь
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    # Хеширование пароля
    hashed_password = hash_password(user.password)
    # Создание нового пользователя
    new_user = User(email=user.email, password=hashed_password, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/info/{user_id}",
    summary="Получить информацию о пользователе",
    response_model=UserResponse
)
async def get_user_info(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.get(
    "/list",
    summary="Получить список зарегистрированных пользователей",
    response_model=list[UserResponse]
)
async def get_user_list(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.put(
    "/update/{user_id}",
    summary="Обновить информацию о пользователе",
    response_model=UserResponse
)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/delete/{user_id}",
    summary="Удалить пользователя"
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db.delete(user)
    db.commit()
    return {"message": "Пользователь успешно удалён"}
