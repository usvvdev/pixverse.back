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
    PATH="${PATH}:/root/.poetry/bin" \
    CHROMEDRIVER_PATH="/usr/local/bin/chromedriver" \
    CHROME_VERSION="136.0.6949.0" \
    CHROMEDRIVER_VERSION="136.0.6949.0"

# Установка необходимых зависимотей включая wget, gnupg, curl, etc.
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    apt-transport-https \
    ca-certificates \
    xvfb \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libxss1 \
    lsb-release \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Add Google Chrome's official GPG key and repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Update package list and install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q --continue -P $CHROMEDRIVER_PATH "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_PATH/chromedriver_linux64.zip -d $CHROMEDRIVER_PATH && \
    rm $CHROMEDRIVER_PATH/chromedriver_linux64.zip

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