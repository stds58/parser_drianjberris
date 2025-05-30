# app/models/__init__.py

from .item import Item
from .search import Search
from app.db.base import Base

# Регистрация моделей в Base.metadata
__all__ = ["Item", "Search"]