**PROJECT STRUCTURE:**

    fastapi_project/
    │
    ├── alembic/                      # Database migration directory (Alembic) Инструмент для миграций базы данных. Связывает модели и физическую структуру БД.
    │   ├── versions/                 # Individual migration scripts
    │   ├── README                    # Migration tool documentation
    │   ├── env.py                    # Alembic environment setup
    │   └── script.py.mako            # Alembic migration script template
    │
    ├── app/                          # Main application package
    │   ├── core/                     # Core settings and configuration
    │   │   │                           (config, settings, main_config) Этот уровень содержит базовые настройки и конфигурации всего приложения, такие как загрузка переменных окружения, подключение к БД, логгирование и т.д.
    │   │   ├── __init__.py
    │   │   ├── config.py             # App settings and environment loading
    │   │
    │   ├── db/                       # Database session and initialization
    │   │   │                           (database, orm, sqlalchemy) Содержит инструменты для работы с базой данных, такие как sessionmaker, engine и базовый класс для моделей
    │   │   ├── __init__.py
    │   │   ├── base.py               # Base class for SQLAlchemy models
    │   │   ├── session_maker.py      # 
    │   │   └── init_db.py            # DB initialization script
    │   │
    │   ├── models/                   # Pydantic/SQLAlchemy models
    │   │   │                           (entities, domain, tables, dto, Data Transfer Object) Содержит SQLAlchemy-модели, описывающие таблицы в БД.
    │   │   ├── __init__.py
    │   │   └─── user.py               # User model definition
    │   │
    │   ├── schemas/                  # Pydantic schemas (data validation)
    │   │   │                           (dto, Data Transfer Objects, serializers, pydantic_models, requests/responses) Содержит Pydantic-модели для валидации входящих и исходящих данных (DTO)
    │   │   ├── __init__.py
    │   │   ├── base.py               #
    │   │   └─── user.py              # User-related request/response schemas
    │   │
    │   ├── crud/                     # CRUD operations (DB interaction logic)
    │   │   │                           (repositories, dao, Data Access Object, data_access, storage) Содержит функции для взаимодействия с БД — операции CRUD (Create, Read, Update, Delete)
    │   │   ├── __init__.py
    │   │   ├── user.py               # User-specific CRUD logic
    │   │
    │   ├── services/                 # Business logic layer
    │   │   │                           (use_cases, business_logic, handlers, interactors, operations, flows) Содержит бизнес-логику приложения, например, проверки, обработку данных и вызов CRUD-операций
    │   │   ├── __init__.py
    │   │   └── user_service.py       # User-specific service functions
    │   │ 
    │   ├── dependencies/             # Dependency injection utilities
    │   │   │                           (deps, auth, utils, middlewares) Содержит утилиты для внедрения зависимостей, например, get_db, аутентификацию, авторизацию.
    │   │   ├── __init__.py
    │   │   ├── get_db.py             # Provides DB session for routes
    │   │   └── user.py               #
    │   ├── api/                      # API route definitions
    │   │   │                           (routers, controllers, endpoints, rest) Содержит маршруты (endpoints) и обработчики HTTP-запросов
    │   │   └── v1/                   # Versioned API (v1)
    │   │      ├── __init__.py
    │   │      └── user.py            # User-related endpoints
    │   │
    │   ├── utils/                    # Helper and utility functions
    │   │   │                           (helpers, tools, lib, functions, shared) Содержит вспомогательные функции, общие для всего приложения.
    │   │   ├── __init__.py
    │   │   └── email.py              # Email sending logic
    │   │ 
    │   └── main.py                   # Entry point of the FastAPI application
    │
    ├── .env                          # Environment variables file
    ├── .gitignore                    # Git ignore rules
    ├── alembic.ini                   # Alembic configuration file
    ├── DEVELOPERS.md                 # Developer guide and instructions
    ├── example.env                   # Example environment config
    ├── README.md                     # Project overview and instructions
    └── requirements.txt              # Python dependencies


    Итоговая иерархия зависимостей:
    alembic → models → db → core  
                   ↓  
        schemas → crud → services → api → dependencies  
                   ↓  
                  utils



    app/core/                 # Конфигурация
       └── app/db/      # Создание Base (базового класса для моделей)
          └── app/models/           # Бизнес-сущности Создание модели (моделей) базы данных
             └── app/schemas/     # Валидация данных Создание Pydantic-схем (валидация данных)
                ├── app/crud/       # CRUD-операции — это базовые операции с БД:
                │   └── manufacturer.py   #getById, getAll, updateById, deleteById
                │                         Create : INSERT INTO ... 
                │                         Read (все записи или по ID) : SELECT * FROM ... WHERE id = ? 
                │                         Update : UPDATE ... WHERE id = ? 
                │                         Delete : DELETE FROM ... WHERE id = ? 
                └── app/services/      # Бизнес-логика Сервисный слой использует CRUD и содержит бизнес-логику — 
                   │                     например, фильтры, проверки, пагинация, преобразования, дополнительные вызовы внешних систем
                   │                     Этот слой отделяет логику от роутера и делает её тестируемой
                   │                                   def register_user(user_data: UserCreate, db: Session):
                   │                                       if user_exists(db, user_data.email):
                   │                                           raise ValueError("Email already exists")
                   │                                       return create_user(db, user_data)
                   │ 
                   └── dependencies/  # Подключение к БД Зависимости Настройка сессии и зависимости (dependency injection)
                      └── app/api/      # API-роуты Создание роутера (API-эндпоинты)

    порядок работы:
    Base — базовый класс для моделей
    Модели БД — описание таблиц
    Pydantic-схемы — валидация данных
    CRUD — операции с БД
    Сервисы — бизнес-логика
    Сессия и зависимости — управление подключением
    Роутеры (API) — HTTP-обработчики


    ┬

                      ┌────────────────────────────────┐
                      │                                │
       alembic<----models<-------db/base.py<----core   │
                      │                          │     │
                      │                          ↓     │
                      │ ┌────────db/session_maker.py   │
                      ↓ ↓                        ↓     ↓
                     crud--->services--->api<--dependencies
                      ↑         ↑
                      │         │
                    [dto]<----schemas






schemas --------> dto -------> crud ---------> services --> api
   ↑               ↑             ↑                ↑          ↑
   |               |             |                |          |
[валидация] [преобразование][работа с БД][бизнес-логика][HTTP маршруты]



