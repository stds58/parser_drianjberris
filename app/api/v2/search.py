from pathlib import Path
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from app.dependencies.get_db import connection
from app.services.search import find_many_search, add_new_search, add_new_items
from app.services.item import delete_all_item
from app.schemas.search import SSearchFilter, SSearchAdd
from sqlalchemy.ext.asyncio import AsyncSession


V2_DIR = Path(__file__).resolve().parent
API_DIR = V2_DIR.parent
APP_DIR = API_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"

router = APIRouter(tags=['Фронтенд'])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/find")
async def get_searches(
        filters: SSearchFilter = Depends(),
        session: AsyncSession = Depends(connection())
    ):
    searchs = await find_many_search(filters=filters, session=session)
    return {"data": searchs}


MODEL_MAP = {
    "search": SSearchAdd
}


@router.get("/stream-data")
async def stream_data(session: AsyncSession = Depends(connection())):
    async def event_generator():
        async for item in add_new_items(session=session):
            yield f"data: {item}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/add")
async def show_add_search_form(request: Request, model: str = "search", session: AsyncSession = Depends(connection())):
    try:
        ModelClass = MODEL_MAP[model]
        db_search = await find_many_search(filters=None, session=session)
        await session.close()
        if len(db_search) > 0:
            phrase = db_search[0].phrase
        else:
            phrase = None
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": ModelClass.model_fields,
            "title": f"Добавить {model}",
            "phrase": phrase
        })
    except ValidationError as e:
        # Ошибки валидации Pydantic
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SSearchAdd.model_fields,
            "title": "Добавить search",
            "form_values": {"a":1},
            "errors": e.errors()
        })
    except (ConnectionRefusedError, OSError, OperationalError) as e:
        await session.rollback()
        error_msg = str(e)
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SSearchAdd.model_fields,
            "title": "Добавить производителя",
            "form_values": {"a":1},
            "errors": [{"loc": ["База данных"], "msg": error_msg}]
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
            "fields": SSearchAdd.model_fields,
            "title": "Добавить search",
            "form_values": {"a":1},
            "errors": [{"loc": ["База данных"], "msg": error_msg}]
        })

@router.post("/add", response_class=HTMLResponse)
async def put_search(request: Request, session: AsyncSession = Depends(connection())):
    try:
        form_data = await request.form()
        await delete_all_item(session=session)
        await add_new_search(data=form_data, session=session)
        return RedirectResponse(url="/frontend/v2/search/add", status_code=303)
    except ValidationError as e:
        # Ошибки валидации Pydantic
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SSearchAdd.model_fields,
            "title": "Добавить search",
            "form_values": dict(form_data),
            "errors": e.errors()
        })
    except (ConnectionRefusedError, OSError, OperationalError) as e:
        await session.rollback()
        error_msg = str(e)
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SSearchAdd.model_fields,
            "title": "Добавить производителя",
            "form_values": dict(form_data),
            "errors": [{"loc": ["База данных"], "msg": error_msg}]
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
            "fields": SSearchAdd.model_fields,
            "title": "Добавить search",
            "form_values": dict(form_data),
            "errors": [{"loc": ["База данных"], "msg": error_msg}]
        })

