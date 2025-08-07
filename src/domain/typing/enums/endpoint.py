# coding utf-8

from enum import StrEnum


class PixverseEndpoint(StrEnum):
    """Перечисление URI эндпоинтов API сервиса PixVerse.

    Содержит пути к основным конечным точкам API для:
    - Генерации контента по тексту
    - Генерации изображений
    - Загрузки медиафайлов
    - Проверки статуса задач

    Все URI указаны относительно базового URL API.
    """

    AUTH = "/creative_platform/login"
    """
    Проверка статуса выполненной генерации.
    """

    TEXT = "/creative_platform/video/t2v"
    """
    Генерация контента по текстовому описанию.
    """

    IMAGE = "/creative_platform/video/i2v"
    """
    Генерация контента по заданой фотографии.
    """

    UPLOAD_IMAGE = "/creative_platform/media/batch_upload_media"
    """
    Загрузка пользовательских изображений для создания контента по фотографии.
    """

    UPLOAD_VIDEO = "/creative_platform/media/upload"

    LAST_FRAME = "/creative_platform/video/frame/last"

    UPLOAD_TOKEN = "/creative_platform/getUploadToken"
    """
    Загрузка пользовательских изображений для создания контента по фотографии.
    """

    STATUS = "/creative_platform/video/list/personal"
    """
    Проверка статуса выполненной генерации.
    """

    TOKEN = "/creative_platform/user/credits"

    RESTYLE = "/creative_platform/video/restyle"

    RESTYLE_TEMPLATE = "/creative_platform/restyle/list"

    TEMPLATES = "/creative_platform/effect/channel/list"


class ChatGPTEndpoint(StrEnum):
    TEXT = "/v1/images/generations"
    """
    Генерация контента по заданой фотографии.
    """

    PHOTO = "/v1/images/edits"
    """
    Генерация контента по заданой фотографии.
    """

    CHAT = "/v1/chat/completions"
    """
    Генерация контента по заданой фотографии.
    """


class TopmediaEndpoint(StrEnum):
    AUTH = "/account/login"

    SLANG = "/v2/voice/text_slang"

    USER = "/v2/user/info"

    SPEECH = "/v5/voice/tts"

    DOWNLOAD = "/v2/user/audition/download/{id}"

    SONG = "/v2/async/text-to-song"

    RESULT = "/v2/task/results"
