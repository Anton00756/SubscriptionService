from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from service.models import Subscription, User
from service.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from service.database import get_db
from service.utils import TokenEngine
from .utils import get_user_from_cookie

router = APIRouter()


@router.post('/new', summary='Оформить подписку', response_model=SubscriptionResponse)
async def create_subscription(
    subscription: SubscriptionCreate, user_mail: str = Depends(get_user_from_cookie), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_mail).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if not user.is_active:
        raise HTTPException(status_code=404, detail='Пользователь не активен')

    # Создаём новую подписку
    new_subscription = Subscription(
        type=subscription.type,
        user_id=user.id,
        name=subscription.name,
        price=subscription.price,
        auto_renew=subscription.auto_renew,
        duration=subscription.duration,
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription


@router.get('/info/{subscription_id}', summary='Получить информацию о подписке', response_model=SubscriptionResponse)
async def get_subscription_info(
    subscription_id: int, db: Session = Depends(get_db), user_mail: str = Depends(get_user_from_cookie)
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail='Подписка не найдена')

    # Проверка, принадлежит ли подписка текущему пользователю
    user = db.query(User).filter(User.email == user_mail).first()
    if subscription.user_id != user.id:
        raise HTTPException(status_code=403, detail='Доступ запрещен')

    return subscription


@router.get('/list', summary='Получить список подписок пользователя', response_model=list[SubscriptionResponse])
async def get_subscription_list(
    request: Request, db: Session = Depends(get_db), user_mail: str = Depends(get_user_from_cookie)
):
    user = db.query(User).filter(User.email == user_mail).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    subscriptions = db.query(Subscription).filter(Subscription.user_id == user.id).all()
    return subscriptions


@router.put('/update/{subscription_id}', summary='Обновить подписку', response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: int,
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
    user_mail: str = Depends(get_user_from_cookie),
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail='Подписка не найдена')

    user = db.query(User).filter(User.email == user_mail).first()
    if subscription.user_id != user.id:
        raise HTTPException(status_code=403, detail='Доступ запрещен')

    # Обновляем данные подписки
    for key, value in subscription_data.model_dump(exclude_unset=True).items():
        setattr(subscription, key, value)

    db.commit()
    db.refresh(subscription)
    return subscription


@router.delete('/cancel/{subscription_id}', summary='Отменить подписку')
async def cancel_subscription(
    subscription_id: int, db: Session = Depends(get_db), user_mail: str = Depends(get_user_from_cookie)
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail='Подписка не найдена')

    user = db.query(User).filter(User.email == user_mail).first()
    if subscription.user_id != user.id:
        raise HTTPException(status_code=403, detail='Доступ запрещен')

    db.delete(subscription)
    db.commit()
    return {'message': 'Подписка успешно отменена'}
