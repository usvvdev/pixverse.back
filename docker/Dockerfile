FROM python:3.11

ENV PROJECT_DIR="/code" \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="${PATH}:/root/.poetry/bin" \
    # chrome
    CHROME_BIN="/usr/bin/google-chrome" \
    CHROMEDRIVER_PATH="/usr/local/bin/chromedriver" \
    DISPLAY=":99"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
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
    libxext6 \
    libxfixes3 \
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

# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -y update && \
    apt-get -y install google-chrome-stable --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver (updated method)
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E 's/.* ([0-9]+)\.[0-9]+\.[0-9]+.*/\1/') && \
    echo "Chrome major version: $CHROME_MAJOR_VERSION" && \
    CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION) && \
    echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION" && \
    wget -q https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Verify installations
RUN echo "Chrome version: $(google-chrome --version)" && \
    echo "ChromeDriver version: $(chromedriver --version)"

# Install Poetry
RUN pip install --upgrade pip==24.0 \
    && pip install poetry==$POETRY_VERSION \
    && poetry --version

# Set working directory
WORKDIR $PROJECT_DIR

# Copy dependency files first for better caching
COPY ./pyproject.toml ./poetry.lock ${PROJECT_DIR}/

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . ${PROJECT_DIR}/

# Set up Xvfb and run the application
ENTRYPOINT ["sh", "./scripts/start.sh"]