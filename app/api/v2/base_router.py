from fastapi import APIRouter
from app.api.v2.search import router as search_router
from app.api.v2.item import router as item_router


v2_router = APIRouter(prefix="/v2")


v2_router.include_router(search_router, prefix="/search", tags=["поиск"])
v2_router.include_router(item_router, prefix="/item", tags=["результат"])


