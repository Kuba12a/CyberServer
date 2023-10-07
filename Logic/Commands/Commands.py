import uuid
from enum import Enum

from pydantic import BaseModel


class Action(Enum):
    FILE_DOWNLOAD = 1,
    LIST_FILES = 2,
    CLIPBOARD_MONITOR = 3,
    DISCONNECT = 4


class Command(BaseModel):
    id: uuid.UUID
    action: Action
    ip_address: str
    parameters: dict
