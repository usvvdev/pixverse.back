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
