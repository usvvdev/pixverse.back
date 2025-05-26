# coding utf-8

from enum import StrEnum


class PixVerseUri(StrEnum):
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

    UPLOAD = "/openapi/v2/image/upload"
    """
    Загрузка пользовательских изображений для создания контента по фотографии.
    """

    STATUS = "/openapi/v2/video/result/{id}"
    """
    Проверка статуса выполненной генерации.
    """
