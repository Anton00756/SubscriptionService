from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from service.database import get_db
from service.models import PaymentMethod, User
from service.schemas.payment_method import PaymentMethodCreate, PaymentMethodResponse, PaymentMethodUpdate
from .utils import get_user_from_cookie

router = APIRouter()


@router.post(
    "/new",
    summary="Добавить способ оплаты",
    response_model=PaymentMethodResponse,
)
async def create_payment_method(
    payment_method: PaymentMethodCreate,
    request: Request,
    db: Session = Depends(get_db),
    user_mail: str = Depends(get_user_from_cookie),
):
    # Получение пользователя из базы
    user = db.query(User).filter(User.email == user_mail).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Создание способа оплаты
    new_payment_method = PaymentMethod(
        type=payment_method.type,
        details=payment_method.details,
        user_id=user.id
    )
    db.add(new_payment_method)
    db.commit()
    db.refresh(new_payment_method)
    return new_payment_method


@router.get(
    "/list",
    summary="Получить список способов оплаты",
    response_model=list[PaymentMethodResponse],
)
async def get_payment_methods_list(
    request: Request,
    db: Session = Depends(get_db),
    user_mail: str = Depends(get_user_from_cookie),
):
    user = db.query(User).filter(User.email == user_mail).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    payment_methods = db.query(PaymentMethod).filter(PaymentMethod.user_id == user.id).all()
    return payment_methods


@router.put(
    "/update/{payment_method_id}",
    summary="Обновить способ оплаты",
    response_model=PaymentMethodResponse,
)
async def update_payment_method(
    payment_method_id: int,
    payment_method_update: PaymentMethodUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user_mail: str = Depends(get_user_from_cookie),
):
    payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()
    if not payment_method:
        raise HTTPException(status_code=404, detail="Способ оплаты не найден")

    user = db.query(User).filter(User.email == user_mail).first()
    if payment_method.user_id != user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    for key, value in payment_method_update.dict(exclude_unset=True).items():
        setattr(payment_method, key, value)

    db.commit()
    db.refresh(payment_method)
    return payment_method


@router.delete(
    "/delete/{payment_method_id}",
    summary="Удалить способ оплаты",
    response_class=Response,
)
async def delete_payment_method(
    payment_method_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user_mail: str = Depends(get_user_from_cookie),
):
    payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()
    if not payment_method:
        raise HTTPException(status_code=404, detail="Способ оплаты не найден")

    user = db.query(User).filter(User.email == user_mail).first()
    if payment_method.user_id != user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    db.delete(payment_method)
    db.commit()
    return Response(status_code=200)
