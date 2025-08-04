# coding utf-8

from typing import Any

from ..conf import app_conf

from functools import wraps

from fastapi import Request

from fastapi.responses import JSONResponse


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


def check_user_tokens(
    method_cost: int,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Извлекаем Request из args или kwargs
            request: Request = kwargs.get("request")
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if request is None:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Request object not found"},
                )

            try:
                body = dict(
                    pair.split("=", 1) for pair in str(request.query_params).split("&")
                )
                data = IPixverseBody(**body)
            except Exception as e:
                return JSONResponse(
                    status_code=422,
                    content={"detail": f"Invalid request body: {e}"},
                )

            if (
                data.app_id == "tea.ai.bundle"
                and data.user_id == "07E241D5-94A4-4A51-AA62-949994D74D89"
            ):
                user = await user_repository.fetch_with_filters(
                    user_id=data.user_id,
                    app_id=data.app_id,
                )
                if user.balance < method_cost:
                    raise PixverseError(
                        402,
                        extra={
                            "Информация о пользователе": f"{data.user_id}\n\n{data.app_id}"
                        },
                    )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
