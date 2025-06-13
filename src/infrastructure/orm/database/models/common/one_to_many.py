# coding utf-8

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table,
)

from ......domain.entities.core import ITable


PixverseApplicationTemplates = Table(
    "pixverse_application_templates",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pixverse_applications.id"),
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

PixverseApplicationStyles = Table(
    "pixverse_application_styles",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pixverse_applications.id"),
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

PhotoGeneratorApplicationTemplates = Table(
    "photo_generator_application_templates",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("photo_generator_applications.id"),
        primary_key=True,
    ),
    Column(
        "template_id",
        Integer,
        ForeignKey(
            "photo_generator_templates.id",
        ),
        primary_key=True,
    ),
)
