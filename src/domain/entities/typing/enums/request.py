# coding utf-8

from enum import StrEnum


class RequestMethod(StrEnum):
    GET = "GET"
    """
    Метод GET - получение ресурса.
    """

    POST = "POST"
    """
    Метод POST - создание ресурса.
    """
