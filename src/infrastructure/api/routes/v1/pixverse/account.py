# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import PixverseAccountView

from ......domain.tools import (
    auto_docs,
    validate_token,
)

from .....factroies.api.v1 import PixverseAccountViewFactory

from ......interface.schemas.api.account import (
    Account,
    IAccount,
    ChangeAccount,
)


pixverse_account_router = APIRouter(tags=["Accounts"])


@pixverse_account_router.get(
    "/accounts",
)
async def fetch_accounts(
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> list[Account]:
    return await view.fetch_accounts(
        token_data,
    )


@pixverse_account_router.get(
    "/accounts/{id}",
)
async def fetch_account(
    id: int,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> Account:
    return await view.fetch_account(
        id,
        token_data,
    )


@pixverse_account_router.post(
    "/accounts",
)
async def add_account(
    data: IAccount,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> ChangeAccount:
    return await view.add_account(
        data,
        token_data,
    )


@pixverse_account_router.put(
    "/accounts/{id}",
)
async def update_account(
    id: int,
    data: ChangeAccount,
    _: str = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> ChangeAccount:
    return await view.update_account(
        id,
        data,
    )


@pixverse_account_router.delete(
    "/accounts/{id}",
)
async def delete_account(
    id: int,
    _: str = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> bool:
    return await view.delete_account(
        id,
    )
