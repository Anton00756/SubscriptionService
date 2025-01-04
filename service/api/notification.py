from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from service.database import get_db
from service.models import Subscription, User
from .utils import get_user_from_cookie

router = APIRouter()


@router.get(
    "/",
    summary="Получить уведомления о предстоящих событиях (автосписания, завершение подписок)",
)
async def get_notifications(
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_user_from_cookie),
):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    subscriptions = db.query(Subscription).filter(Subscription.user_id == user.id).all()
    notifications = []

    for subscription in subscriptions:
        # Пример проверки: завершение подписки через 3 дня
        if subscription.days_left <= 3:
            notifications.append(
                {
                    "type": "subscription_end",
                    "message": f"Подписка {subscription.type} истекает через {subscription.days_left} дня(ей).",
                }
            )

    return notifications
