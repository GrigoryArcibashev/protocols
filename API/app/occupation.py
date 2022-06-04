import dataclasses
from typing import Optional


@dataclasses.dataclass
class Occupation:
    name: Optional[str]
    type: Optional[str]

    def __str__(self):
        return f'{self.name} ({self.type})'
