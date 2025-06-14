# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from ......domain.entities.core import ITable


class UserGenerations(ITable):
    uuid: int = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    generation_id: int = Column(
        Integer,
        nullable=False,
        unique=True,
    )
    account_id: int = Column(
        Integer,
        nullable=False,
    )
