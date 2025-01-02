import logging

import uvicorn
from fastapi import FastAPI

from api import *


app = FastAPI(
    docs_url="/api/docs",
)

app.include_router(user_router, prefix="/user", tags=["Пользователи"])
app.include_router(subscription_router, prefix="/subscription", tags=["Подписки"])
app.include_router(payment_router, prefix="/payment", tags=["Платежи"])
app.include_router(payment_method_router, prefix="/payment_method", tags=["Способы оплаты"])
app.include_router(notification_router, prefix="/notification", tags=["Уведомления"])


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        log_level=logging.DEBUG,
        reload=True
    )
