from enum import Enum

from pydantic import BaseModel
import datetime


class Status(str, Enum):
    ADDED = "added"
    CONNECTED = "connected"


class Agent(BaseModel):
    id: int
    ip_address: str
    created_at: datetime.datetime
    encryption_key: str
    cookie: str
    status: Status
