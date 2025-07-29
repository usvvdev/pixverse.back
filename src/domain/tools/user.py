# coding utf-8

from typing import Any

from ..conf import app_conf

from fastapi import Depends

from ..entities.core import (
    IConfEnv,
    IWebhook,
    ISchema,
)

from ..errors import PixverseError

from ...interface.schemas.external import UsrData

from ...interface.schemas.external.body import IPixverseBody

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import (
    UserDataRepository,
    ApplicationRepository,
)

conf: IConfEnv = app_conf()


user_repository = UserDataRepository(
    IDatabase(conf),
)

application_repository = ApplicationRepository(
    IDatabase(conf),
)


async def add_user_tokens(
    data: IWebhook,
) -> ISchema:
    application_data: (
        Any | None
    ) = await application_repository.fetch_application_by_bundle_id(
        "application_id",
        data.app.bundle_id,
        ["products"],
    )

    if application_data is None:
        return None

    matched_product = next(
        (
            product
            for product in application_data.products
            if product.name == data.event.properties.product_id
        ),
        None,
    )

    if matched_product is None:
        return None

    user = await user_repository.fetch_with_filters(
        user_id=data.user.user_id,
        app_id=data.app.bundle_id,
    )

    user_data = UsrData(
        user_id=user.user_id if user is not None else data.user.user_id,
        app_id=user.app_id if user is not None else data.app.bundle_id,
        balance=int(
            user.balance if user is not None else 0 + matched_product.tokens_amount,
        ),
    )

    return await user_repository.create_or_update_user_data(
        user_data,
    )


async def fetch_user_tokens(
    data: IPixverseBody = Depends(),
):
    user = await user_repository.fetch_with_filters(
        user_id=data.user_id,
        app_id=data.app_id,
    )
    if user.balance == 0:
        raise PixverseError(402)

    body = UsrData(
        user_id=user.id,
        app_id=user.app_id,
        balance=int(
            user.balance + 10,
        ),
    )

    return await user_repository.update_record(
        user.id,
        body,
    )
