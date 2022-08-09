# Сервис записи через тг-бота с веб-администрированием

##  Содержание

1. [Описанеие проекта](#Description)
2. [Программынй стек](#Moduls)
3. [Установка](#Install) 
4. [Структура репозиторя бекенда](#Struct) 
5. [Сруктура репозитория бота](#StructBot) 

## Описание проекта <a name="Description"></a>
Веб сервис в котором пользователи могут настраивать своего ТГ бота для записи клиентов на мероприятия, тренировки, встречи  и т.д. Каждый пользователь сервиса сможет получить информацию по всем записям в веб-интерфейсе.  
Соотвественно клиенты(сотрудники и т.д) смогут записываться через интерактивный интерфейс ТГ бота (https://habr.com/ru/post/666278/)

## Программный стек <a name="Moduls"></a>

- Flask 2.0
- Flask-SQLAlchemy
- Flask-RESTPlus (Swagger)
- Flask-Blueprint
- Flask-WTF
- Flask-Admin
- Aiogram
- React - в данном репозитории не присутствует, используется для Frontend



## Установка проекта <a name="Install"></a>
Перед установкой убедитесь, что у вас установлен PostgreSQL, Python 3.8

```
git clone https://gitlab.mai.ru/IOEliseev/oleg_invest
source ./back/env/bit/activate

pip install back/requirements.txt

flask db init
flask db migrate
flask db upgarde

python3 main.py
python3 main_bot.py 
```

## Структура репозитория бекенда <a name="Struct"></a>
```
.
├── app.py
|
├── config_bot.json
├── main_bot.py
├── main.py
|
├── models
│   ├── all_models.py
│   └── __init__.py
├── requirements.txt
├── routers
│   ├── admin_tools.py
│   └── namespace
│       ├── booking_ns
│       │   ├── booking_ns.py
│       │   ├── booking_schema.py
│       │   ├── dataclass_booking.py
│       │   └── queries_booking.py
│       ├── client_ns
│       │   ├── client_ns.py
│       │   ├── queries.py
│       │   ├── schema.py
│       │   └── validate.py
│       ├── event_ns
│       │   ├── dataclass_event.py
│       │   ├── event_ns.py
│       │   ├── event_schema.py
│       │   └── queries_event.py
│       ├── __init__.py
│       ├── service_ns
│       │   ├── queries.py
│       │   ├── schema.py
│       │   ├── service_ns.py
│       │   └── validate.py
│       ├── staff_ns
│       │   ├── queries.py
│       │   ├── schema.py
│       │   ├── staff_ns.py
│       │   └── validate.py
│       └── users_ns
│           ├── queries.py
│           ├── shema.py
│           ├── users_ns.py
│           └── validate.py
├── setting_web.py
└── tree.text
```

## Структура репозитория бот <a name="StructBot"></a>
```
.
├── bots_setting
│   ├── bot_elements
│   │   ├── cancel.py
│   │   ├── getters
│   │   │   ├── __init__.py
│   │   │   ├── register_getters.py
│   │   │   └── services_getters.py
│   │   ├── __init__.py
│   │   ├── output
│   │   │   ├── __init__.py
│   │   │   └── services_output.py
│   │   ├── register
│   │   │   ├── __init__.py
│   │   │   ├── register_check.py
│   │   │   └── user_register.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── sign_up_for_services.py
│   │   ├── setters
│   │   │   ├── __init__.py
│   │   │   └── register_setters.py
│   │   └── storages
│   │       ├── __init__.py
│   │       └── register_storages.py
│   ├── bots.py
│   ├── config.json
│   └── main.py
```




