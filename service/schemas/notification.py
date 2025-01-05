from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    subscription_id: int
    message: str
    days_left: int


class NotificationResponse(NotificationCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True