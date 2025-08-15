#!/bin/bash

ENV_FILE=".env"

# Загружаем конфигурацию
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: Configuration file '$ENV_FILE' not found."
    exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

# Проверка переменных
: "${APP_SERVICE:?APP_SERVICE is not set in .env}"
: "${APP_HOST:?APP_HOST is not set in .env}"
: "${APP_PORT:?APP_PORT is not set in .env}"

echo "INFO: Running FastAPI service '$APP_SERVICE' on ${APP_HOST}:${APP_PORT}"

# Запуск FastAPI
uvicorn "services.${APP_SERVICE}.main:main" --reload --factory --host "${APP_HOST}" --port "${APP_PORT}"
