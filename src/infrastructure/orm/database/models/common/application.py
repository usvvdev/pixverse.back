# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)

from datetime import datetime

from ......domain.entities.core import ITable


class Applications(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    application_id: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    description: str = Column(
        String,
        nullable=True,
    )
    region: str = Column(
        String,
        nullable=True,
    )
    store_region: str = Column(
        String,
        nullable=True,
    )
    application_number: str = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    category: str = Column(
        String,
        nullable=True,
    )
    start_date: datetime = Column(
        DateTime,
        nullable=True,
    )
    release_date: datetime = Column(
        DateTime,
        nullable=True,
    )
    technology: str = Column(
        String,
        nullable=True,
    )
