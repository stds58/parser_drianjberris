# GITFLOW

## 1 клонирование репозитория с гитхуба
**создаём папку и скачиваем в неё все репозитории**  
**всегда используем командную строку или терминал IDE  
(через интерфейс IDE может не сработать):**

    git clone https://github.com/cabinet/<имя репозитория>.git

## 2 питон
**используем питон 3.13. проверка версии питона:**

    python --version

**активируем окружение**

    windows:
        .venv\scripts\activate

    linux:
        source venv/bin/activate

**обновляем pip**

    python.exe -m pip install --upgrade pip
    

## 3 внесение изменений в гитхуб. наименование веток и коммитов
**создать свою ветку и сразу на неё переключиться**

    git checkout -b feature/<имя ветки>

**переключиться на нужную ветку**

    git checkout feature/<имя ветки>

**добавить файл в staging:**

    git add <имя_файла>
    например: 
        git add GITFLOW.md
 
**формат названия веток:**

    Общий формат: <тип>/<описание> или <тип>/<номер_задачи>-<описание>.
    Примеры:
        feature/login    - для разработки новых функций
        bugfix/login-bug - для исправления ошибок

**типы веток:**

    main                — стабильная версия, готовая к проду
    develop             — ветка для интеграции новых функций перед релизом
    test                - ветка для тестов
    feature/<имя ветки> — ветки для разработки отдельных функций

**формат сообщения коммита:**

    <тип>(<область>): <краткое описание. можно по-русски>
    Примеры:
        feat: добавить сильный пароль
        fix: исправить ошибку загрузки файла
        docs: обновить руководство

**типы коммитов:**

    feat     — новая функциональность.
    fix      — исправление ошибки.
    chore    — мелкие правки, не влияющие на логику.
    docs     — изменения документации.
    style    — изменения форматирования кода.
    refactor — рефакторинг без изменения поведения.
    test     — добавление тестов.     

**закомитить**

    git commit -m "<>:<>"
    например: 
        git commit -m "feat: README.md"
    либо добавить все изменения и закоммитить одной командой
        git commit -a -m "feat: README.md"

**внесение изменений в гитхуб**

    git push

**загрузить ветку**

    git pull

**переключиться на нужную ветку**

    git checkout feature/<имя ветки>

**периодически обновляем свою ветку изменениями из ветки develop  
(после того, как кто-нибудь сделает merge в develop)**

    git checkout feature
    git fetch origin
    git rebase origin/develop


## 4 открываем pull request 



## 5 зависимости
**установить зависимости из requirements**

    pip install -r requirements.txt


**добавить зависимости в requirements**

    pip freeze > requirements.txt
    



**первый запуск**

    docker network create mynetwork
    docker-compose down -v
    docker-compose build --no-cache
    docker-compose up

**последующие**

    docker-compose up --build

**alembic**

    alembic revision --autogenerate -m "Auto-generated migration"
    alembic upgrade head

## ошибки
**ошибка**

    ERROR:    [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): 
    обычно разрешается только одно использование адреса сокета

    Это приводит к тому, что FastAPI не может запуститься нормально , и поэтому:
    Не вызывается dependency() из connection() и тд

**решение: убить все питоновские процессы**

    netstat -ano | findstr :8000
    taskkill /PID <ваш_PID> /F


