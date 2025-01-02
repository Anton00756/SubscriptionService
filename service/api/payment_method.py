from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/new",
    summary="Добавить способ оплаты"
)
async def create_payment_method():
    return {}


@router.get(
    "/list",
    summary="Получить список способов оплаты"
)
async def get_payment_methods_list():
    return {}


@router.put(
    "/update",
    summary="Обновить способ оплаты"
)
async def update_payment_method():
    return {}


@router.delete(
    "/delete",
    summary="Удалить способ оплаты"
)
async def delete_payment_method():
    return {}
