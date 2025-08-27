from enum import Enum, auto
import uuid
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone


class Status(Enum):
    ENABLED = auto()
    JUNK = auto()


class File(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: Status = Field(default=Status.ENABLED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name != 'updated_at':
            object.__setattr__(self, 'updated_at', datetime.now(timezone.utc))
