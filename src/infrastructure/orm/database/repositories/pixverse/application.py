# coding utf-8

from sqlalchemy import delete, insert

from ...models import (
    PixverseApplications,
    PixverseTemplates,
    PixverseStyles,
)

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class PixverseApplicationRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PixverseApplications,
        )

    async def fetch_all(
        self,
        related: list[str],
    ) -> PixverseApplications:
        return await self.fetch_one_to_many(
            related=related,
        )

    async def fetch_application(
        self,
        field_name: str,
        value: str,
        related: list[str],
    ) -> PixverseApplications | None:
        return await self.fetch_one_to_many(
            field_name,
            value,
            many=False,
            related=related,
            models=(PixverseTemplates, PixverseStyles),
            model_filter=lambda v: v.is_active,
        )

    async def update_application(
        self,
        application_id: int,
        relation_table,
        relation_ids: list[int],
        relation_column_name: str,
    ):
        async for session in self._engine.get_session():
            await session.execute(
                delete(relation_table).where(
                    relation_table.c.application_id == application_id
                )
            )

            # Добавляем новые связи, если они есть
            if relation_ids:
                await session.execute(
                    insert(relation_table),
                    [
                        {"application_id": application_id, relation_column_name: rel_id}
                        for rel_id in relation_ids
                    ],
                )

            await session.commit()
