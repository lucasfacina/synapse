from pydantic import field_validator

from domain.errors.common.empty import EmptyValueError
from domain.value_objects.base import ValueObject


class Description(ValueObject[str]):
    @field_validator('value')
    @classmethod
    def validate(self, v: str):
        if not v or not v.strip():
            raise EmptyValueError('descrição')
        return v.strip()
