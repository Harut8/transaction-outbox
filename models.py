from enum import Enum

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column
from db import BaseModel


class OutboxStatus(Enum):
    FAILED = -1
    PENDING = 0
    PROCESSED = 1


class OutboxMessage(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[OutboxStatus] = mapped_column(default=OutboxStatus.PENDING)
    payload: Mapped[dict | list] = mapped_column(JSON)
    routing_key: Mapped[str]
