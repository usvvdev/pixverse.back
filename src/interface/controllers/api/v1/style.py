# coding utf-8

from .....infrastructure.orm.database.repositories import PixverseStyleRepository

from ....schemas.api import (
    Style,
    ChangeStyle,
    IStyle,
)


class PixverseStyleController:
    def __init__(
        self,
        repository: PixverseStyleRepository,
    ) -> None:
        self._repository = repository

    async def fetch_styles(
        self,
    ) -> list[Style]:
        return await self._repository.fetch_all()

    async def fetch_style_by_template_id(
        self,
        template_id: int,
    ) -> Style | None:
        return await self._repository.fetch_style(
            "template_id",
            template_id,
        )

    async def fetch_style_by_id(
        self,
        id: int,
    ) -> Style | None:
        return await self._repository.fetch_style(
            "id",
            id,
        )

    async def add_style(
        self,
        data: IStyle,
        preview_small: str,
        preview_large: str,
    ) -> ChangeStyle:
        return await self._repository.add_record(
            ChangeStyle(
                **data.dict,
                preview_small=preview_small,
                preview_large=preview_large,
            ),
        )

    async def update_style(
        self,
        id: int,
        data: Style,
        preview_small: str,
        preview_large: str,
    ) -> ChangeStyle:
        return await self._repository.update_record(
            id,
            ChangeStyle(
                **data.dict,
                preview_small=preview_small,
                preview_large=preview_large,
            ),
        )

    async def delete_style(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )
