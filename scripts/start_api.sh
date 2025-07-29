#!/bin/bash

load_config() {
    local env_file=".env"

    if [ ! -f "$env_file" ]; then
        echo "ERROR" "Configuration file '$env_file' not found."
        return 1
    fi

    if export $(grep -v '^#' "$env_file" | xargs) > /dev/null 2>&1; then
        echo "INFO" "Application configuration has been loaded successfully."
    fi
}

# Функция для запуска приложения
start_fastapi_app() {
    echo "INFO" "Running Application."
    uvicorn "$@"
}

load_config

start_fastapi_app services.${APP_SERVICE}.main:main --reload --factory --host ${APP_HOST} --port ${APP_PORT}
# start_fastapi_app services.cosmetic.main:main --reload --factory --host ${APP_HOST} --port ${APP_PORT}