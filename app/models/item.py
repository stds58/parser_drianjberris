from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from sqlalchemy import ForeignKey

# alembic revision --autogenerate -m "Auto-generated migration"

class Item(Base):
    id_search: Mapped[int] = mapped_column(ForeignKey("search.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(info={"verbose_name": "наименование"})
    brand: Mapped[str] = mapped_column(info={"verbose_name": "бренд"})
    price_u: Mapped[float] = mapped_column(info={"verbose_name": "цена в копейках"})
    sale_price_u: Mapped[float] = mapped_column(info={"verbose_name": "цена со скидкой в копейках"})
    feedbacks: Mapped[int] = mapped_column(info={"verbose_name": "количество отзывов"})
    rating: Mapped[int] = mapped_column(info={"verbose_name": "рейтинг"})
    #search: Mapped["Search"] = relationship("Search", back_populates="item", lazy="selectin")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "price_u": self.price_u,
            "sale_price_u": self.sale_price_u,
            "feedbacks": self.feedbacks,
            "rating": self.rating,
            "id_search": self.id_search
        }

    def to_html(self):
        return f"""
            <div class="product-card">
                <h4>{self.name}</h4>
                <p><strong>Бренд:</strong> {self.brand}</p>
                <p><strong>Цена:</strong> {self.price_u // 100} ₽</p>
                <p><strong>Рейтинг:</strong> ⭐{self.rating} ({self.feedbacks} отзывов)</p>
                <hr>
            </div>
        """

