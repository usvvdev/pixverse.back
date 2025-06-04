# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from .....domain.entities.core import ITable


class PixverseTemplates(ITable):
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
    category: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    preview_small: str = Column(
        String,
        nullable=False,
    )
    preview_large: str = Column(
        String,
        nullable=False,
    )
