FROM python:3.11

ENV PROJECT_DIR="/code" \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CHACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="${PATH}:/root/.poetry/bin"

# Установка необходимых зависимотей включая wget, gnupg, curl, etc.
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    apt-transport-https \
    ca-certificates \
    xvfb \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --upgrade pip==24.0 \
    && pip install poetry==$POETRY_VERSION \
    && poetry --version 

# Установка рабочей директории
WORKDIR $PROJECT_DIR

# Копирование пакетов
COPY ./pyproject.toml ./poetry.lock ${PROJECT_DIR}/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копирование проекта
COPY . ${PROJECT_DIR}/

# Запуск FastAPI приложения
ENTRYPOINT ["sh", "./scripts/start.sh"]