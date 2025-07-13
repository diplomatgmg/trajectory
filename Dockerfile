FROM python:3.13-alpine AS base
FROM base AS builder

ARG APP_PATH=/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=${APP_PATH}/src \
    PATH="${APP_PATH}/.venv/bin:$PATH"

WORKDIR ${APP_PATH}

RUN apk update \
    && apk add --no-cache uv \
    && rm -rf /var/cache/apk/*


# ============================ #
#        DEPS INSTALLING       #
# ============================ #
FROM builder AS deps-base

COPY pyproject.toml uv.lock ./


FROM deps-base AS deps-dev

RUN uv sync --frozen --dev

FROM deps-base AS deps-prod
# This is test task.


# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM deps-dev AS development

COPY ./src ${APP_PATH}/src

CMD ["hupper", "-m", "src.main", "-w", "src/main.py"]

