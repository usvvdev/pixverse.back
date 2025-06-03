# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from .....domain.entities.core import ITable


class PixverseStyles(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    template_id: int = Column(
        Integer,
        nullable=True,
        primary_key=True,
    )
    prompt: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    name: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    preview: str = Column(
        String,
        nullable=False,
    )
