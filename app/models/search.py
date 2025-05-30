from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Search(Base):
    phrase: Mapped[str] = mapped_column(info={"verbose_name": "строка запроса"})

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, phrase={self.phrase!r})"

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"