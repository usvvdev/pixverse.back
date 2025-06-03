# coding utf-8

from typing import Any

from sqlalchemy import (
    Result,
    ScalarResult,
    Executable,
    ColumnElement,
    select,
    insert,
    delete,
    update,
)

from .base import ISchema

from .table import ITable

from .engine import IEngine


class IRepository:
    def __init__(
        self,
        engine: IEngine,
        model: ITable,
    ) -> None:
        self._engine = engine
        self._model = model

    async def __commit_changes(
        self,
        query: Executable,
    ) -> None:
        async for session in self._engine.get_session():
            await session.execute(
                query,
            )
            await session.commit()

    async def __session_result(
        self,
        query: Executable,
    ) -> ScalarResult | None:
        async for session in self._engine.get_session():
            result: Result = await session.execute(
                query,
            )
            return result.scalars()

    async def __fetch_records(
        self,
        query: Executable,
        many: bool = True,
    ) -> list[Any] | Any | None:
        scalars: ScalarResult = await self.__session_result(
            query,
        )
        return scalars.all() if many else scalars.first()

    async def fetch_all(
        self,
    ) -> list[Any] | None:
        return await self.__fetch_records(
            select(self._model),
        )

    async def fetch_one(
        self,
    ) -> Any | None:
        return await self.__fetch_records(
            select(self._model),
            many=False,
        )

    async def fetch_field(
        self,
        field_name: str,
        value: Any,
        many: bool = True,
    ) -> Any | None:
        condition: ColumnElement = getattr(self._model, field_name)
        return await self.__fetch_records(
            select(self._model).where(
                condition.in_(value) if isinstance(value, list) else condition == value
            ),
            many=many,
        )

    async def add_record(
        self,
        data: ISchema,
    ) -> ISchema:
        await self.__commit_changes(
            insert(self._model).values(
                **data.dict,
            ),
        )
        return data

    async def update_record(
        self,
        id: int,
        data: ISchema,
    ) -> ISchema:
        try:
            await self.__commit_changes(
                update(self._model)
                .filter_by(id=id)
                .values(
                    **data.dict,
                ),
            )
        except Exception as err:
            raise err
        finally:
            True

    async def delete_record(
        self,
        id: int,
    ):
        await self.__commit_changes(
            delete(self._model).filter_by(
                id=id,
            ),
        )
