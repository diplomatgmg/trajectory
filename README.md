# Trajectory — тестовое задание
### [Ссылка на тестовое задание](https://gist.github.com/DGSR/e6ae3504f693aa7a9c1856bb6cf5c5a4)

## Описание

Этот проект — решение тестового задания для работы с расписаниями. Он реализует:
- Получение расписания с внешнего API;
- Логику поиска занятых, свободных и ближайших временных слотов;
- Валидацию и обработку ошибок;
- Покрытие тестами клиентского и сервисного слоя.

## Структура проекта

```
trajectory/
├── src/
│   ├── main.py                # Точка входа, пример использования сервисов
│   ├── clients/               # Клиенты для работы с внешними API
│   │   └── schedule/          # ScheduleClient — клиент расписания
│   ├── services/              # Бизнес-логика (ScheduleService)
│   │   └── schedule/
│   ├── schemas/               # Pydantic-схемы для валидации данных
│   └── logger/                # Конфигурация и фабрика логгера
├── tests/                     # Тесты (pytest)
├── Dockerfile                 # Сборка контейнера
├── docker-compose.yml         # Описание сервисов для разработки и тестирования
├── Makefile                   # Удобные команды для разработки
├── pyproject.toml             # Зависимости и настройки
└── uv.lock                    # Лок-файл зависимостей
```

## Быстрый старт

### 1. Клонирование и подготовка окружения

```bash
# Клонируйте репозиторий и перейдите в папку проекта
cd trajectory

# Установите uv (https://github.com/astral-sh/uv) если не установлен
pip install uv
```

### 2. Запуск в dev-режиме

```bash
make test-dev
```
- Создаст виртуальное окружение, соберёт контейнеры, запустит проект в режиме разработки.

### 3. Запуск тестов

```bash
make test
```
- Запустит тесты внутри контейнера, сгенерирует отчёт о покрытии в директории `tests/htmlcov`.

### 4. Проверка стиля и типов

```bash
make lint      # Проверка линтером и форматтером
make lint-fix  # Автоисправление линтером и форматтером
```

## Описание модулей

### src/main.py
Пример использования ScheduleClient и ScheduleService: получение расписания, поиск занятых/свободных/доступных слотов. Можно доработать под CLI/API.

### src/clients/
- **base.py** — базовый клиент для httpx.AsyncClient.
- **schedule/schedule.py** — ScheduleClient: асинхронно получает расписание с внешнего API.

### src/services/
- **schedule/schedule.py** — ScheduleService: бизнес-логика поиска слотов, проверки доступности, обработки ошибок.
- **schedule/exceptions.py** — Кастомные исключения для сервиса расписания.

### src/schemas/
- **common.py** — Миксин для временных промежутков с валидацией.
- **schedule.py** — Pydantic-схемы: Day, TimeSlot, Schedule, FreeTimeSlot, AvailableTimeSlot.

### src/logger/
- **config.py, enums.py, factory.py** — Конфигурирование и инициализация логгера, поддержка уровней логирования через переменные окружения.

### tests/
- Покрытие тестами клиента, сервисного слоя, схем. Используется pytest, pytest-asyncio, respx (моки).

## Зависимости

- Python >= 3.13
- httpx, pydantic, pydantic-settings, uvloop
- Для разработки: hupper, isort, mypy, ruff
- Для тестов: pytest, pytest-asyncio, pytest-cov, respx

Все зависимости фиксируются через `pyproject.toml` и `uv.lock`.

## Переменные окружения

- `ENV_MODE` — режим запуска проекта (production, development)
- `LOG_LEVEL` — уровень логирования (DEBUG, INFO, WARN, ERROR)
- `ENV_PROJECT_NAME` — имя проекта для docker-compose


## Тестирование

- Покрытие тестами клиента, сервисов, схем (pytest, respx, unittest.mock)
- Для локального запуска: `make test`
- Для просмотра покрытия: откройте `tests/htmlcov/index.html`

---

### P.S
- ИИ использовал только для фундамента. Без слепого копирования
- Cursor использовал только для генерации этого README.md
- Gemini - Частичная генерация тестов, + сторонний взгляд на реализацию бизнес логики
