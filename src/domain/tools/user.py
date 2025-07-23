# coding utf-8

from typing import Any

from ..conf import app_conf

from ..entities.core import IConfEnv

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import (
    UserDataRepository,
)

from ...interface.schemas.api import (
    IUserData,
)

conf: IConfEnv = app_conf()


user_repository = UserDataRepository(
    IDatabase(conf),
)


async def add_user_tokens(
    user_id: Any,
    app_id: str,
):
    user = await user_repository.fetch_with_filters(
        user_id=user_id,
        app_id=app_id,
    )
    data = IUserData(
        user_id=user_id,
        app_id=app_id,
        balance=100,
    )
    if user is not None:
        return await user_repository.update_record(
            user.id,
            data,
        )
