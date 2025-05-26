# coding utf-8

from enum import IntEnum

from fastapi import status


class ErrorCode(IntEnum):
    """
    Перечисление кодов HTTP ошибок.

    Атрибуты:
        unauthorized (int): Код ошибки 401 — Неавторизован.
    """

    unauthorized: int = status.HTTP_401_UNAUTHORIZED
