# coding utf-8

from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
)

from sqlalchemy.dialects.mysql import TINYINT

from ......domain.entities.core import ITable


class AuthUsers(ITable):
    uuid: str = Column(
        String,
        default=uuid4(),
        nullable=False,
        primary_key=True,
    )
    username: str = Column(
        String(length=150),
        nullable=False,
        primary_key=True,
    )
    email: str = Column(
        String(length=254),
        nullable=False,
        primary_key=True,
    )
    is_active: int = Column(
        TINYINT,
        default=1,
        nullable=False,
    )
    password: str = Column(
        String(length=128),
        nullable=False,
    )
