"""модели Pydantic  https://habr.com/ru/companies/amvera/articles/851642/"""
from pydantic import BaseModel, ConfigDict


class BaseConfigModel(BaseModel):
    """https://docs.pydantic.dev/latest/api/config/"""
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Удалять начальные и конечные пробелы для типов str
        from_attributes=True,       # Разрешить работу с ORM-объектами
        populate_by_name=True,      # Разрешить использование алиасов
        use_enum_values=True,       # Использовать значения ENUM вместо объектов
        extra="ignore",             # Игнорировать лишние поля
        max_recursion_depth=1,
    )

class BaseFilter(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore"  # Позволяет игнорировать лишние поля
        #extra="forbid"  # Запретить передачу лишних полей
    )


