# coding utf-8

from ..models import Applications, PixverseTemplates

from .....domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class ApplicationRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            Applications,
        )

    async def fetch_application(
        self,
        field_name: str,
        value: str,
    ) -> Applications | None:
        return await self.fetch_template_fields(
            "templates",
            PixverseTemplates,
            loader_filter=lambda v: v.is_active == True,
            model_filter=getattr(self._model, field_name) == value,
            many=False,
        )

    async def fetch_all(
        self,
    ) -> Applications:
        return await self.fetch_template_fields(
            "templates",
            PixverseTemplates,
            filter=lambda v: v.is_active == True,
        )
