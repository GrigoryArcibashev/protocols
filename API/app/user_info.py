import dataclasses
from typing import Optional

from app.occupation import Occupation


@dataclasses.dataclass
class UserInfo:
    id: str
    first_name: str
    last_name: str
    birth_date: Optional[str]
    country: Optional[str]
    city: Optional[str]
    occupation: Optional[Occupation]
    langs: Optional[list[str]]
    interests: Optional[str]

    def __str__(self):
        result = f'{self.first_name} {self.last_name} (id{self.id})\n'
        if self.birth_date is not None:
            result += f'\t| Дата рождения: {self.birth_date}\n'
        if self.country is not None:
            result += f'\t| Страна: {self.country}\n'
        if self.city is not None:
            result += f'\t| Город: {self.city}\n'
        if self.occupation is not None:
            result += f'\t| Занятость: {str(self.occupation)}\n'
        if self.langs is not None:
            result += f'\t| Языки: {", ".join(self.langs)}\n'
        if self.interests is not None:
            result += f'\t| Интересы: {self.interests}\n'
        return result
