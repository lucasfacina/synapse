from dataclasses import dataclass, field
from file import File


@dataclass
class City(File):
    descripton: str
    uf: str
