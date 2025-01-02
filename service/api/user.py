from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/register",
    summary="Зарегистрировать пользователя"
)
async def register_user():
    return {}


@router.get(
    "/info",
    summary="Получить информацию о пользователе"
)
async def get_user_info():
    return {}


@router.get(
    "/list",
    summary="Получить список зарегистрированных пользователей"
)
async def get_user_list():
    return {}


@router.put(
    "/update",
    summary="Обновить информацию о пользователе"
)
async def update_user():
    return {}


@router.delete(
    "/delete",
    summary="Удалить пользователя"
)
async def delete_user():
    return {}
