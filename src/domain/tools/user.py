# coding utf-8

from typing import Any

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
    try:
        application_data: (
            Any | None
        ) = await application_repository.fetch_application_by_bundle_id(
            "application_id",
            data.app.bundle_id,
            ["products"],
        )

        print(application_data.__dict__)

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

        print(matched_product)

        if matched_product is None:
            return None

        user_data = UsrData(
            user_id=data.user.user_id,
            app_id=data.app.bundle_id,
            balance=matched_product.tokens_amount,
        )

        return await user_repository.create_or_update_user_data(
            user_data,
        )

    except Exception:
        pass
