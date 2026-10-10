# 🖥️ Система управления виртуальными ресурсами

**Студент:** Чувилов Александр Александрович, группа ЭФБО-07-24
**Преподаватель:** Ящун Татьяна Викторовна

Учебный проект по дисциплине «Технологии разработки приложений на базе фреймворков». Проект развивается от работы к работе: консольный скрипт (ПР1), функции и JSON (ПР2), объектная модель (ПР3) веб-интерфейс на Django (ПР5) и система шаблонов Django (ПР6).

## 🎯 Назначение

Приложение предназначено для учёта виртуальных ресурсов (виртуальных машин с CPU, RAM и дисковым пространством) и заявок пользователей на их выделение. Консольная версия приложения (ПР3) дополнена веб-интерфейсом на Django (ПР5), страницы которого с ПР6 формируются шаблонами Django.

В веб-интерфейсе можно:
* видеть сводку на главной странице: число ресурсов, активные заявки, средний объём RAM, общую стоимость и последние заявки;
* просматривать каталог виртуальных ресурсов с доступностью на текущую дату и сортировкой по объёму RAM;
* просматривать страницу ресурса: характеристики, расчёт стоимости аренды по составляющим и заявки на этот ресурс;
* просматривать список заявок с фильтром «все / активные / отменённые»;
* просматривать страницу заявки: дату, пользователя, его email, статус и сведения о ресурсе.

В консольной версии дополнительно доступны:
* поиск ресурсов по названию и проверка вместимости по RAM;
* добавление пользователей;
* проверка доступности ресурса на любую дату;
* создание и отмена заявок;
* статистика по ресурсам;
* хранение данных между запусками.

## 🛠️ Используемые технологии

* Python 3;
* Django 5.2 – веб-фреймворк;
* Django Template Language (DTL) – шаблоны страниц;
* HTML – разметка веб-страниц;
* CSS и Bootstrap 5.3 – оформление страниц;
* JavaScript – клиентское поведение интерфейса;
* pytest – автоматизированные тесты;
* flake8 – проверка качества кода.

## 👥 Целевая аудитория

Системные администраторы и DevOps-инженеры, а также владельцы проектов, которым нужно отслеживать выделенные вычислительные ресурсы, пользователей и стоимость аренды.

## 📦 Предметная область

Основными объектами предметной области являются:
* виртуальный ресурс;
* пользователь;
* заявка на выделение ресурса.

Пользователь может создавать заявки на выделение ресурсов на определённые даты. Один ресурс не может иметь две активные заявки на одну и ту же дату. Отменённая заявка не блокирует ресурс и позволяет создать новую заявку на эту дату.

## 🧩 Основные сущности

### Resource – виртуальный ресурс

Объект `Resource` представляет виртуальную машину, доступную для выделения.

Основные атрибуты:
* `id` – уникальный идентификатор ресурса;
* `name` – название ресурса;
* `cpu_cores` – число ядер CPU;
* `ram_gb` – объём оперативной памяти, ГБ;
* `storage_gb` – объём дискового пространства, ГБ.

Основные методы:
* `is_suitable_for()` – проверка достаточности RAM;
* `calculate_monthly_cost()` – расчёт ежемесячной стоимости аренды;
* `validate_ram()` – статический метод проверки значения RAM;
* `__str__()` – строковое представление ресурса.

### User – пользователь

Объект `User` представляет пользователя системы.

Основные атрибуты:
* `id` – уникальный идентификатор пользователя;
* `name` – имя пользователя;
* `email` – адрес электронной почты.

Основные методы:
* `from_data()` – создание объекта `User` из набора данных;
* `__str__()` – строковое представление пользователя.

### Allocation – заявка на выделение ресурса

Объект `Allocation` представляет заявку пользователя на выделение ресурса.

Основные атрибуты:
* `id` – уникальный идентификатор заявки;
* `resource` – объект `Resource`;
* `allocation_date` – дата выделения;
* `user` – объект `User`;
* `is_cancelled` – признак отмены заявки.

Основные методы:
* `cancel()` – отмена заявки;
* `__str__()` – строковое представление заявки.

## 🌐 Страницы веб-интерфейса

| URL | Имя маршрута | View-функция | Шаблон |
|---|---|---|---|
| `/` | `homepage:index` | `index()` | `homepage/index.html` |
| `/resources/` | `resources:list` | `resources()` | `resources/resource_list.html` |
| `/resources/<int:resource_id>/` | `resources:detail` | `resource_detail()` | `resources/resource_detail.html` |
| `/allocations/` | `allocations:list` | `allocations()` | `allocations/allocation_list.html` |
| `/allocations/<int:allocation_id>/` | `allocations:detail` | `allocation_detail()` | `allocations/allocation_detail.html` |

Если ресурс или заявка с указанным идентификатором не найдены, страница выводит сообщение «не найден» и возвращает код статуса 404.

## 🎨 Шаблоны Django (ПР6)

HTML-код вынесен из Python в шаблоны. View-функция загружает данные из JSON, формирует контекст и вызывает `render(request, "шаблон.html", context)`:

```text
View → Context → Template → HTML
```

Используемые возможности Django Template Language:
* базовый шаблон `templates/base.html` с блоками `{% block title %}` и `{% block content %}`;
* наследование шаблонов `{% extends "base.html" %}`;
* включаемые шаблоны `{% include %}`: навигация (`templates/includes/navigation.html`), карточка ресурса (`resources/includes/resource_card.html`), статус заявки (`allocations/includes/allocation_status.html`);
* передача данных через контекст;
* циклы `{% for %}` с блоком `{% empty %}` и условия `{% if %}` / `{% else %}`;
* именованные URL и пространства имён (`app_name`): `{% url 'resources:detail' resource.id %}`;
* фильтры `length`, `default`, `date`, `floatformat`, `lower` и тег `{% widthratio %}`;
* подсветка активного раздела меню через `request.resolver_match.app_name`;
* статические файлы `{% load static %}`: собственный CSS (`style.css`), JavaScript (`main.js`: текущий год в подвале и переход по клику на строку таблицы) и изображение (`logo.png`) в `homepage/static/homepage/`.

Параметры отображения передаются через GET-параметры ссылок, без форм: `/resources/?sort=ram`, `/allocations/?status=active`, `/allocations/?status=cancelled`.

Каталог шаблонов уровня проекта `templates/` подключён в `settings.py` через параметр `DIRS` списка `TEMPLATES`.

## ⚙️ Основные операции

### Используется в веб-интерфейсе (ПР5, ПР6)

* сводная статистика по ресурсам (`get_resources_statistics()`);
* сортировка ресурсов по RAM (`sort_resources()`);
* просмотр списка ресурсов;
* просмотр информации о ресурсе;
* просмотр списка заявок;
* просмотр информации о заявке;
* проверка доступности ресурса на текущую дату.

### Отложено до следующих работ

Эти операции реализованы в ПР3 и работают в консольной версии. В веб-интерфейсе они появятся, когда будут добавлены формы и POST-запросы:

* добавление ресурса;
* поиск ресурса по названию;
* проверка вместимости;
* фильтрация ресурсов по RAM;
* создание заявки;
* отмена заявки;
* создание пользователя;
* поиск пользователя.

## 💾 Хранение данных

Данные приложения хранятся в JSON-файлах:
* `data/resources.json`;
* `data/users.json`;
* `data/allocations.json`.

При загрузке данные из JSON преобразуются в объекты `Resource`, `User` и `Allocation`. При сохранении объекты преобразуются в данные JSON.

Для связи заявки с ресурсом и пользователем в `allocations.json` используются их идентификаторы `resource_id` и `user_id`.

## 🗂️ Структура проекта

```text
virtual-resources-manager/
│
├── README.md
├── requirements.txt
├── manage.py
├── main.py
├── storage.py
├── utils.py
│
├── templates/
│   ├── base.html
│   └── includes/
│       └── navigation.html
│
├── vrm/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── homepage/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/homepage/index.html
│   └── static/homepage/
│       ├── css/style.css
│       ├── js/main.js
│       └── img/logo.png
│
├── resources/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/resources/
│       ├── resource_list.html
│       ├── resource_detail.html
│       └── includes/resource_card.html
│
├── allocations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/allocations/
│       ├── allocation_list.html
│       ├── allocation_detail.html
│       └── includes/allocation_status.html
│
├── models/
│   ├── __init__.py
│   ├── resource.py
│   ├── user.py
│   └── allocation.py
│
├── data/
│   ├── resources.json
│   ├── users.json
│   └── allocations.json
│
└── tests/
    ├── test_resources.py
    ├── test_users.py
    ├── test_allocations.py
    └── test_views.py
```

## 📚 Назначение модулей

### `main.py`

Консольная версия приложения (сохранена с ПР3). Отвечает за запуск консольного приложения, отображение меню, получение данных от пользователя и организацию пользовательских сценариев.

### `vrm/`

Пакет настроек Django-проекта:
* `settings.py` – настройки проекта;
* `urls.py` – маршрутизация верхнего уровня;
* `asgi.py`, `wsgi.py` – точки взаимодействия с сервером.

### `homepage/`

Django-приложение, отвечающее за главную страницу:
* `views.py` – view-функция `index()`, вызывающая `render()`;
* `urls.py` – маршрут главной страницы (`app_name = "homepage"`);
* `templates/homepage/index.html` – шаблон главной страницы;
* `static/homepage/` – общие статические файлы проекта: CSS, JavaScript и логотип.

Функция `page()` из ПР5 удалена: общий HTML-каркас страниц теперь находится в `templates/base.html`.

### `resources/`

Django-приложение, отвечающее за ресурсы:
* `views.py` – view-функции `resources()` и `resource_detail()`;
* `urls.py` – маршруты приложения (`app_name = "resources"`);
* `templates/resources/` – шаблоны списка, страницы и карточки ресурса;
* `models.py` – Django-модели (заполняется в следующих работах).

### `allocations/`

Django-приложение, отвечающее за заявки:
* `views.py` – view-функции `allocations()` и `allocation_detail()`;
* `urls.py` – маршруты приложения (`app_name = "allocations"`);
* `templates/allocations/` – шаблоны списка, страницы заявки и статуса заявки;
* `models.py` – Django-модели (заполняется в следующих работах).

Для пользователей отдельное Django-приложение не создаётся: Django предоставляет встроенную модель User в `django.contrib.auth`.

### `models/`

Классы предметной области и функции работы с ними (пакет ПР3):
* `resource.py` – класс `Resource` и функции работы с ресурсами;
* `user.py` – класс `User` и функции работы с пользователями;
* `allocation.py` – класс `Allocation` и функции работы с заявками.

### `storage.py`

Отвечает за загрузку и сохранение данных. Выполняет преобразование JSON → объекты Python и объекты Python → JSON.

### `utils.py`

Вспомогательные функции консольного ввода:
* `input_int()` – безопасный ввод целого числа;
* `input_date()` – безопасный ввод даты.

### `tests/`

Автоматизированные тесты проекта: тесты предметной области (ПР3) и тесты веб-страниц `test_views.py` (ПР6) – коды ответов, 404, используемые шаблоны и фильтр заявок.

## ▶️ Запуск приложения

Подготовка (один раз):
```text
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

На Windows активация окружения: `venv\Scripts\activate`.

Веб-версия (Django):
```text
python manage.py runserver
```

После запуска открыть в браузере адрес:
```text
http://127.0.0.1:8000/
```

Запускать нужно из корня проекта: пути к файлам `data/*.json` относительные.

Консольная версия (сохранена):
```text
python main.py
```

## ✅ Тестирование

Для запуска автоматизированных тестов выполнить:
```text
pytest -v
```

## 🔍 Проверка качества кода

Для проверки соответствия кода требованиям PEP 8 используется `flake8`. Каталог виртуального окружения исключается из проверки:
```text
flake8 . --extend-exclude=venv
```

Проверка работоспособности Django-проекта:
```text
python manage.py check
```

## 📌 Зависимости

Состав зависимостей в `requirements.txt`:
* `Django==5.2.*` – веб-фреймворк;
* `pytest` – автоматизированные тесты;
* `flake8` – проверка качества кода.

## 🔧 Git

Исходный код проекта хранится в Git-репозитории. Для проверки состояния репозитория:
```text
git status
```

Каждый коммит, относящийся к ПР6, начинается с метки `PR6:`. Пример:
```text
git commit -m "PR6: add Django templates and static files"
```

## 🚀 Текущее состояние и план развития

Реализовано (ПР5):
* Django-проект и три Django-приложения (`homepage`, `resources`, `allocations`);
* маршрутизация URL двух уровней;
* view-функции и страницы;
* отображение данных предметной области (ресурсы и заявки);
* проверка доступности ресурса через логику ПР3.

Реализовано (ПР6):
* Django Template Language, базовый шаблон `base.html`, наследование шаблонов и блоки `block`;
* включаемые шаблоны `include`;
* передача данных через контекст, циклы и условия;
* именованные URL и пространства имён;
* фильтры шаблонов;
* статические файлы: собственные CSS, JavaScript и изображение;
* отказ от функции `page()`, оформление Bootstrap 5.3 и собственные стили;
* главная страница со статистикой, сортировка ресурсов, фильтр заявок по статусу, расчёт стоимости на странице ресурса;
* тесты веб-страниц.

Данные по-прежнему хранятся в JSON, Django ORM и формы пока не используются.

Планируется:
* перенос сущностей `Resource`, `User` и `Allocation` в Django ORM;
* подключение базы данных;
* формы создания и редактирования заявок;
* использование отложенной логики ПР3 (`create_allocation()`, `cancel_allocation()`, `add_resource()`, поиск и сортировка);
* разработка API;
* контейнеризация приложения;
* настройка CI/CD.

## 🧮 Функции по сущностям

Сущность Resource – ресурс (ПР3):

| Имя функции | Файл расположения | Назначение |
|---|---|---|
| `Resource` (класс) | `models/resource.py` | ресурс: атрибуты id, name, cpu_cores, ram_gb, storage_gb |
| `is_suitable_for()` | `models/resource.py` | проверка достаточности RAM |
| `calculate_monthly_cost()` | `models/resource.py` | расчёт ежемесячной стоимости аренды |
| `validate_ram()` | `models/resource.py` | статический метод проверки значения RAM |
| `__str__()` | `models/resource.py` | строковое представление ресурса |
| `add_resource()` | `models/resource.py` | создание объекта Resource и добавление его в коллекцию |
| `find_resource()` | `models/resource.py` | поиск объектов Resource по названию |
| `find_resource_by_id()` | `models/resource.py` | поиск объекта Resource по идентификатору; используется веб-страницей ресурса |
| `check_resource_capacity()` | `models/resource.py` | поиск ресурса и проверка его вместимости по RAM |
| `filter_resources_by_ram()` | `models/resource.py` | отбор объектов Resource по объёму RAM |
| `sort_resources()` | `models/resource.py` | сортировка коллекции объектов Resource; используется списком ресурсов (`?sort=ram`) |
| `get_resources_statistics()` | `models/resource.py` | статистика по ресурсам; используется главной страницей |

Сущность User – пользователь (ПР3):

| Имя функции | Файл расположения | Назначение |
|---|---|---|
| `User` (класс) | `models/user.py` | пользователь: атрибуты id, name, email |
| `from_data()` | `models/user.py` | создание объекта User из набора данных JSON |
| `__str__()` | `models/user.py` | строковое представление пользователя |
| `add_user()` | `models/user.py` | создание объекта User и добавление его в коллекцию |
| `find_user()` | `models/user.py` | поиск объектов User по имени или адресу электронной почты |
| `find_user_by_id()` | `models/user.py` | поиск объекта User по идентификатору |

Сущность Allocation – заявка (ПР3):

| Имя функции | Файл расположения | Назначение |
|---|---|---|
| `Allocation` (класс) | `models/allocation.py` | заявка: атрибуты id, resource, user, allocation_date, is_cancelled |
| `date` (свойство) | `models/allocation.py` | дата выделения как объект date для фильтра `date` в шаблонах (добавлено в ПР6) |
| `cancel()` | `models/allocation.py` | отмена заявки (установка признака is_cancelled) |
| `__str__()` | `models/allocation.py` | строковое представление заявки |
| `find_allocation_by_id()` | `models/allocation.py` | поиск объекта Allocation по идентификатору (добавлена в ПР5); используется веб-страницей заявки |
| `is_resource_available()` | `models/allocation.py` | проверка доступности ресурса с учётом активных заявок; используется веб-страницей ресурса |
| `create_allocation()` | `models/allocation.py` | проверка доступности, создание объекта Allocation и добавление его в коллекцию |
| `cancel_allocation()` | `models/allocation.py` | поиск заявки и вызов её метода cancel() |
| `get_resource_status()` | `models/allocation.py` | формирование сообщения о доступности ресурса |

Хранение данных (`storage.py`, ПР3):

| Имя функции | Назначение |
|---|---|
| `load_resources()` | загрузка `data/resources.json`: JSON → объекты Resource; используется веб-страницами ресурсов |
| `save_resources()` | сохранение `data/resources.json`: объекты Resource → JSON |
| `load_users()` | загрузка `data/users.json`: JSON → объекты User |
| `save_users()` | сохранение `data/users.json`: объекты User → JSON |
| `load_allocations()` | загрузка `data/allocations.json`: JSON → объекты Allocation; используется веб-страницами ресурсов и заявок |
| `save_allocations()` | сохранение `data/allocations.json`: объекты Allocation → JSON |

Веб-слой (ПР5):

| Приложение | Имя функции | Файл расположения | Назначение |
|---|---|---|---|
| homepage | `page()` | `homepage/views.py` | единый каркас HTML-страницы: кодировка, заголовок, Bootstrap 5.3, навигация |
| homepage | `index()` | `homepage/views.py` | главная страница `/` |
| resources | `resources()` | `resources/views.py` | страница `/resources/`: список ресурсов из `data/resources.json` |
| resources | `resource_detail()` | `resources/views.py` | страница `/resources/<int:resource_id>/`; если ресурс не найден – код статуса 404 |
| allocations | `allocations()` | `allocations/views.py` | страница `/allocations/`: список заявок из `data/allocations.json` |
| allocations | `allocation_detail()` | `allocations/views.py` | страница `/allocations/<int:allocation_id>/`; если заявка не найдена – код статуса 404 |

Функции сущностей и хранилища используются одновременно консольной и веб-версией приложения: view-функции ПР5 вызывают `load_resources()`, `load_users()`, `load_allocations()`, `find_resource_by_id()` и `find_allocation_by_id()` вместо консольных сценариев `main.py`.
