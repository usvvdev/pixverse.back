# coding utf-8

from ..conf import app_conf

from ..entities.core import (
    IConfEnv,
    IWebhook,
    ISchema,
)

from ...interface.schemas.external import UsrData

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import (
    UserDataRepository,
)

conf: IConfEnv = app_conf()


user_repository = UserDataRepository(
    IDatabase(conf),
)


async def add_user_tokens(
    data: IWebhook,
) -> ISchema:
    body = UsrData(
        user_id=data.user.user_id,
        app_id=data.app.bundle_id,
        balance=100,
    )

    return await user_repository.create_or_update_user_data(
        body,
    )
