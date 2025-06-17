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

# Функция для запуска задачи
start_celery_task() {
    echo "INFO" "Running Job."
    celery "$@"
}

load_config


start_celery_task -A services.jobs.${TASK_APP}.celery worker --beat --loglevel=info --scheduler celerybeat-schedule-${TASK_APP}
