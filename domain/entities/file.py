from enum import Enum, auto


class Status(Enum):
    ENABLED = auto()
    JUNK = auto()


class File:
    def __init__(self, entity_name, data):
        self.entity_name = entity_name
        self.data = data
        self.data['status'] = Status.ENABLED

    @property
    def status(self):
        return self.data.get('status')

    @status.setter
    def status(self, value: Status):
        self.data['status'] = value

    def __repr__(self):
        return f"{self.entity_name}(data='{self.data}')"
