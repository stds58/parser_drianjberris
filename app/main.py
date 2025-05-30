from fastapi import FastAPI, HTTPException
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

#from app.models import Item
#from app.schemas import ItemCreate, ItemResponse
from sqlalchemy.orm import Session
#from app.database import engine, Base, AsyncSessionLocal, get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy import text
#from app  all import connection, Product, get_db
from app.api.v1.base_router import v1_router
from app.api.v2.base_router import v2_router
from fastapi.staticfiles import StaticFiles

#app = FastAPI(debug=settings.DEBUG)
app = FastAPI(debug=settings.DEBUG, title="API", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http://localhost:8000/api/v1/search/find/
# http://localhost:8000/frontend/v2/search/add/

app.include_router(v1_router, prefix="/api")
app.include_router(v2_router, prefix="/frontend")

@app.get("/test")
def test():
    return {"message": "ttttttttttttttt"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)