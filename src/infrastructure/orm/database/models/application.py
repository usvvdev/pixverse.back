# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from .application_templates import ApplicationTemplates

from .....domain.entities.core import ITable


class Applications(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    app_id: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )

    templates = relationship(
        "PixverseTemplates",
        secondary=ApplicationTemplates,
        back_populates="applications",
    )
