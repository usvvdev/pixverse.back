# coding utf-8

from ...models import UserData

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......interface.schemas.external import UsrData


class UserDataRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            UserData,
        )

    async def create_or_update_user_data(
        self,
        body: UsrData,
    ):
        user_data: UserData = await self.fetch_with_filters(
            user_id=body.user_id,
            app_id=body.app_id,
        )
        if user_data is not None:
            return await self.update_record(
                user_data.id,
                data=UsrData(
                    user_id=body.user_id,
                    app_id=body.app_id,
                    app_id_usage=int(1 + user_data.app_id_usage),
                ),
            )
        return await self.add_record(body)
