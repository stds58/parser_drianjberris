from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, fk_cascade
from sqlalchemy import Index


class Item(Base):
    id_search = Mapped[fk_cascade] = mapped_column( Index("idx_search") )
    name = Mapped[str] = mapped_column(Index("idx_name"), info={"verbose_name": "наименование"})
    brand = Mapped[str] = mapped_column(Index("idx_brand"), info={"verbose_name": "бренд"})
    price_u = Mapped[float] = mapped_column(info={"verbose_name": "цена в копейках"})
    sale_price_u = Mapped[float] = mapped_column(info={"verbose_name": "цена со скидкой в копейках"})
    feedbacks = Mapped[int] = mapped_column(info={"verbose_name": "количество отзывов"})
    rating = Mapped[int] = mapped_column(info={"verbose_name": "рейтинг"})
    search: Mapped["Search"] = relationship("Search", back_populates="item", lazy="selectin")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

