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


    # @field_validator("phone_number", mode='before')
    # def validate_phone_number(cls, value):
    #     if not re.match(r'^\d{2,3}$', value):
    #         raise ValueError('производитель должен содержать от 2 до 3 цифр')
    #     return value

    # @field_validator("date_of_birth", mode='before')
    # def validate_date_of_birth(cls, value):
    #     if value and value >= datetime.now().date():
    #         raise ValueError('Дата рождения должна быть в прошлом')
    #     return value

    # @model_validator(mode='after')
    # def check_age(self):
    #     today = date.today()
    #     age = today.year - self.birthday_date.year - (
    #             (today.month, today.day) < (self.birthday_date.month, self.birthday_date.day))
    #
    #     if age < 18:
    #         raise ValueError("Пользователь должен быть старше 18 лет")
    #     if age > 120:
    #         raise ValueError("Возраст не может превышать 120 лет")
    #     return self
    #
    # @model_validator(mode='after')
    # def set_default_name(self):
    #     if self.name.strip() == '':
    #         self.name = f"User_{self.id}"
    #     return self

