from fastapi import APIRouter
from app.api.auth.keycloak import router as keycloak_router

auth_router = APIRouter()


auth_router.include_router(keycloak_router)