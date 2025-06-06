# coding utf-8

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table,
)

from .....domain.entities.core import ITable


ApplicationTemplates = Table(
    "application_templates",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("applications.id"),
        primary_key=True,
    ),
    Column(
        "template_id",
        Integer,
        ForeignKey(
            "pixverse_templates.id",
        ),
        primary_key=True,
    ),
)

ApplicationStyles = Table(
    "application_styles",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("applications.id"),
        primary_key=True,
    ),
    Column(
        "style_id",
        Integer,
        ForeignKey(
            "pixverse_styles.id",
        ),
        primary_key=True,
    ),
)
