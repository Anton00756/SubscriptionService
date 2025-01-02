from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/new",
    summary="Создать платёж"
)
async def create_payment():
    return {}


@router.get(
    "/list",
    summary="Получить список платежей пользователя"
)
async def get_payment_list():
    return {}


@router.post(
    "/set_status",
    summary="Изменить статус платежа"
)
async def set_payment_status():
    return {}
