from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    summary="Получить уведомления о предстоящих событиях (автосписания, завершение подписок)"
)
async def get_notifications():
    return {}
