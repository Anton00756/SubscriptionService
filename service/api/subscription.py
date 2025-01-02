from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/new",
    summary="Оформить подписку"
)
async def create_subscription():
    return {}


@router.get(
    "/info",
    summary="Получить информацию о подписке"
)
async def get_subscription_info():
    return {}


@router.get(
    "/list",
    summary="Получить список подписок пользователя"
)
async def get_subscription_list():
    return {}


@router.put(
    "/update",
    summary="Обновить подписку"
)
async def update_subscription():
    return {}


@router.delete(
    "/cancel",
    summary="Отменить подписку"
)
async def cancel_subscription():
    return {}
