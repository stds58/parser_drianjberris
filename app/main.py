from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.base_router import v1_router
from app.api.v2.base_router import v2_router


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

@app.get("/")
async def redirect_to_frontend():
    return RedirectResponse(url="/frontend/v2/search/add")

app.include_router(v1_router, prefix="/api")
app.include_router(v2_router, prefix="/frontend")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)