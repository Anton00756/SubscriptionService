from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from service.database import get_db
from service.models import Notification, Subscription, User
from service.schemas.notification import NotificationResponse
from .utils import get_user_from_cookie

router = APIRouter()


@router.get(
    "/notifications",
    summary="Получить уведомления о подписках",
    response_model=list[NotificationResponse],
)
async def get_notifications(
    db: Session = Depends(get_db),
    user_mail: str = Depends(get_user_from_cookie),
):
    # Находим пользователя
    user = db.query(User).filter(User.email == user_mail).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем активные подписки пользователя
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == user.id, Subscription.is_active.is_(True)
    ).all()

    # Создаем уведомления
    notifications = []
    for subscription in subscriptions:
        # Вычисляем оставшиеся дни
        end_date = subscription.end_date
        days_left = max((end_date - datetime.now()).days, 0)

        # Создаем уведомление
        message = f"Подписка {subscription.name} истекает через {days_left} дней."
        new_notification = Notification(
            user_id=user.id,
            subscription_id=subscription.id,
            message=message,
            days_left=days_left,
        )
        db.add(new_notification)
        notifications.append(new_notification)

    # Сохраняем уведомления в БД
    db.commit()

    return notifications
