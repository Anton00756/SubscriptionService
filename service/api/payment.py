from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from service.database import get_db
from service.models import Payment, User
from service.schemas.payment import PaymentCreate, PaymentResponse, PaymentStatusUpdate
from .utils import get_user_from_cookie

router = APIRouter()


@router.post(
    "/new",
    summary="Создать платёж",
    response_model=PaymentResponse,
)
async def create_payment(
    payment: PaymentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_user_from_cookie),
):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_payment = Payment(
        amount=payment.amount,
        status=payment.status,  # Статус платежа по умолчанию
        user_id=user.id
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get(
    "/list",
    summary="Получить список платежей пользователя",
    response_model=list[PaymentResponse],
)
async def get_payment_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_user_from_cookie),
):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    payments = db.query(Payment).filter(Payment.user_id == user.id).all()
    return payments


@router.post(
    "/set_status",
    summary="Изменить статус платежа",
    response_model=PaymentResponse,
)
async def set_payment_status(
    payment_status_update: PaymentStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_user_from_cookie),
):
    payment = db.query(Payment).filter(Payment.id == payment_status_update.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Платёж не найден")

    user = db.query(User).filter(User.email == current_user).first()
    if payment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    payment.status = payment_status_update.status
    db.commit()
    db.refresh(payment)
    return payment
