from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.database import get_db
from service.models import Subscription, User, Payment
from .utils import get_user_from_cookie

router = APIRouter()


@router.get('/', summary='Получить уведомления о предстоящих событиях (завершение подписок)')
async def get_notifications(
    db: Session = Depends(get_db),
    user_mail: str = Depends(get_user_from_cookie),
):
    # Получаем пользователя
    user = db.query(User).filter(User.email == user_mail).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    # Получаем все платежи пользователя
    payments = db.query(Payment).filter(Payment.user_id == user.id).order_by(Payment.open_date.desc()).all()

    notifications = []

    for payment in payments:
        # Находим связанную подписку
        subscription = db.query(Subscription).filter(Subscription.id == payment.subscription_id).first()
        if not subscription:
            continue

        # Вычисляем дату окончания подписки
        subscription_end_date = payment.open_date + timedelta(days=subscription.duration)

        # Вычисляем оставшиеся дни
        days_left = (subscription_end_date - datetime.now()).days
        # Добавляем уведомление, если подписка скоро истекает
        # if days_left <= 3:
        notifications.append(
            {
                'type': 'subscription_end',
                'message': f"Подписка '{subscription.name}' истекает через {days_left} дня(ей).",
                'subscription_id': subscription.id,
                'subscription_end_date': subscription_end_date.strftime('%Y-%m-%d'),
            }
        )

    return notifications
