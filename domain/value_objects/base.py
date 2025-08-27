from typing import TypeVar, Generic
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')


class ValueObject(BaseModel, Generic[T]):
    model_config = ConfigDict(frozen=True)

    value: T

    def __str__(self) -> str:
        return str(self.value)


class CompositeValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)
