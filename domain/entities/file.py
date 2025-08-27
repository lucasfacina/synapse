from enum import Enum, auto
import uuid
from dataclasses import dataclass, field


class Status(Enum):
    ENABLED = auto()
    JUNK = auto()


@dataclass
class File:
    id: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    status: Status = field(default=Status.ENABLED, kw_only=True)
