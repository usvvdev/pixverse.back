# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from ..common import (
    PixverseApplicationStyles,
    PixverseApplicationTemplates,
    PixverseApplicationCatagories,
)

from ......domain.entities.core import ITable


class PixverseApplications(ITable):
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
        secondary=PixverseApplicationTemplates,
        back_populates="applications",
    )

    styles = relationship(
        "PixverseStyles",
        secondary=PixverseApplicationStyles,
        back_populates="applications",
    )

    categories = relationship(
        "PixverseCategories",
        secondary=PixverseApplicationCatagories,
        back_populates="applications",
    )
