#!/bin/bash

# Load application configuration
load_app_conf() {
    local env_file=".env"
    
    if [[ ! -f "${env_file}" ]]; then
        echo "ERROR: Configuration file '${env_file}' not found." >&2
        return 1
    fi

    # Load all variables except comments
    while IFS= read -r line; do
        [[ -z "${line}" || "${line}" =~ ^# ]] && continue
        export "${line?}"
    done < "${env_file}"

    echo "INFO: Application configuration loaded successfully"
    return 0
}

# Start Celery worker with beat scheduler
start_celery_worker() {
    local app_name="services.jobs.${TASK_APP}.celery"
    local schedule_file="/tmp/celerybeat-${TASK_APP}.db"
    
    echo "INFO: Starting Celery worker for ${TASK_APP}"
    
    # Start Celery with file-based scheduler
    celery -A "${app_name}" worker \
        --beat \
        --loglevel="info" \
        --schedule="${schedule_file}"
}

# Main execution
main() {
    load_app_conf || exit 1
    start_celery_worker
}

main "$@"