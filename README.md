# Привет всем, я [Степан](https://daniilshat.ru/) ![](https://github.com/blackcater/blackcater/raw/main/images/Hi.gif)

## Описание backend части для платформы — **Pixverse**

Основной стек приложения: `FastAPI`, `Pydantic`, `Selenium`, `Httpx`

### Этапы разработки:

#### 1. Изучение API платформы Pixverse

Я обнаружил, что для интеграции подойдут следующие HTTP эндпоинты:

* `/creative_platform/login`
* `/creative_platform/video/t2v`
* `/creative_platform/video/i2v`

Они позволили реализовать бизнес-логику:

* Авторизация на платформе
* Создание видео на основе текста (T2V)
* Создание видео на основе изображения и текста (I2V)

Для запросов я использовал `httpx`, благодаря чему легко реализовал получение `access_token` через `/creative_platform/login`, который далее использовался при генерации видео.

#### 2. Работа с изображениями и статусами генерации

API предоставляет возможность загружать изображения и получать статус генерации видео. Это было реализовано с помощью `httpx` и запросов к:

* `/openapi/v2/image/upload`
* `/openapi/v2/video/result/{id}`

#### 3. Генерация через Selenium

Для симуляции пользовательского взаимодействия и получения логов от сервера я использовал `Selenium`. Это позволило отправлять промпты (prompt) и обрабатывать асинхронные ответы.

#### 4. Интеграция в FastAPI

Все модули были объединены и связаны с помощью `FastAPI`, создавая REST API интерфейс.

---

### 📦 Примеры кода API:

#### Авторизация

```python
@pixverse_router.post("/auth")
@auto_docs(
    "api/v1/t2v",
    "POST",
    description="Роутер для аутентификации на платформе.",
    params={
        "username": {"type": "string", "description": "Имя аккаунта"},
        "password": {"type": "string", "description": "Пароль аккаунта"},
    },
)
async def auth_user(
    body: OAuth2PasswordRequestForm = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> AccessToken:
    user = await view.auth_user(body)
    try:
        return AccessToken(access_token=user.response.result.token)
    except Exception:
        raise InvalidCredentials
```

#### Генерация видео по тексту

```python
@pixverse_router.post("/t2v")
@auto_docs(...)
async def text_to_video(
    body: IBody = Depends(),
    token: str = Depends(oauth2_scheme),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    return await view.text_to_video(token, body)
```

#### Генерация видео по изображению

```python
@pixverse_router.post("/i2v")
@auto_docs(...)
async def image_to_video(
    token: str = Depends(oauth2_scheme),
    body: IBody = Depends(),
    file: UploadFile = File(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    return await view.image_to_video(token, body, file)
```

#### Получение статуса генерации

```python
@pixverse_router.post("/status")
@auto_docs(...)
async def generation_status(
    body: StatusBody = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    return await view.generation_status(body)
```

---

### 📁 Структура URI:

```python
class PixVerseUri(StrEnum):
    AUTH = "/creative_platform/login"
    TEXT = "/creative_platform/video/t2v"
    IMAGE = "/creative_platform/video/i2v"
    UPLOAD = "/openapi/v2/image/upload"
    STATUS = "/openapi/v2/video/result/{id}"
```

---

### 🌐 HTTP клиент с httpx:

```python
class Web3:
    def __init__(self, url: str) -> None:
        self._url = url

    async def get_client(self, headers: dict[str, Any]) -> AsyncGenerator[AsyncClient, Any]:
        async with AsyncClient(headers=headers) as client:
            yield client

    async def __make_request(...):
        ...

    async def send_request(...):
        ...
```

### 🎬 Клиент PixVerse:

```python
class PixVerseCore(Web3):
    def __init__(self):
        super().__init__(PIXVERSE_API_URL)

    async def post(...):
        ...

    async def get(...):
        ...
```

```python
class PixVerseClient:
    def __init__(self, core: PixVerseCore):
        self.core = core

    async def generate_video_from_text(...):
        ...

    async def generate_video_from_image(...):
        ...
```

---

### ✅ Заключение:

Проект охватывает все ключевые этапы интеграции с Pixverse API: от авторизации до получения финального результата генерации. Архитектура построена модульно, легко расширяется и сопровождается, что делает её подходящей для реальных production-решений.


