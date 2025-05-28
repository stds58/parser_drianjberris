from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.dependencies.get_db import connection
from app.services.item import find_many_item, add_one_item
from app.schemas.item import SItemFilter, SItemAdd
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError


V2_DIR = Path(__file__).resolve().parent
API_DIR = V2_DIR.parent
APP_DIR = API_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"

router = APIRouter(tags=['Фронтенд'])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/find")
async def get_items(
        filters: SItemFilter = Depends(),
        session: AsyncSession = Depends(connection())
    ):
    items = await find_many_item(filters=filters, session=session)
    return {"data": items}


MODEL_MAP = {
    "item": SItemAdd
}

@router.get("/add")
async def show_add_form(request: Request, model: str = "item"):
    ModelClass = MODEL_MAP[model]
    return templates.TemplateResponse("dynamic_form.html", {
        "request": request,
        "fields": ModelClass.model_fields,
        "title": f"Добавить {model}"
    })

@router.post("/add", response_class=HTMLResponse)
async def put_search(request: Request, session: AsyncSession = Depends(connection())):
    try:
        form_data = await request.form()
        item_data = SItemAdd(**dict(form_data))

        db_item = await add_one_item(data=item_data, session=session)

        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SItemAdd.model_fields,
            "title": "Добавить item",
            "form_values": dict(form_data),
            "data": db_item
        })
    except ValidationError as e:
        # Ошибки валидации Pydantic
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SItemAdd.model_fields,
            "title": "Добавить item",
            "form_values": dict(form_data),
            "errors": e.errors()
        })

    except IntegrityError as e:
        # Ошибки целостности данных (включая уникальные ограничения)
        await session.rollback()
        error_msg = str(e.orig)
        if isinstance(e.orig, UniqueViolationError):
            error_msg = f"Уже существует запись: {error_msg}"
            print('error_msg ',error_msg)

        # Передаём ошибку в шаблон
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SItemAdd.model_fields,
            "title": "Добавить item",
            "form_values": dict(form_data),
            "errors": [{"loc": ["База данных"], "msg": error_msg}]
        })