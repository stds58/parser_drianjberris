from fastapi import APIRouter
from app.api.v1.search import router as search_router
from app.api.v1.item import router as item_router


# Основной роутер для версии v1
v1_router = APIRouter(prefix="/v1")

# Подключение модульных роутеров
v1_router.include_router(search_router, prefix="/search", tags=["поиск"])
v1_router.include_router(item_router, prefix="/item", tags=["результат"])


