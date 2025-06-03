# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)

from ...views.v1 import PixverseAccountView

from .....domain.tools import auto_docs, validate_token

from ....factroies.api.v1 import PixverseAccountViewFactory

from .....interface.schemas.api.account import Account


account_router = APIRouter(tags=["Accounts"])


@account_router.get(
    "/accounts",
)
async def fetch_accounts(
    _: str = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> list[Account]:
    return await view.fetch_accounts()


@account_router.get(
    "/account/{id}",
)
async def fetch_account(
    id: int,
    _: str = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> Account:
    return await view.fetch_account(
        id,
    )


@account_router.post(
    "/account",
)
async def add_account(
    data: Account,
    _: str = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
):
    return await view.add_account(
        data,
    )


@account_router.put(
    "/account/{id}",
)
async def update_account(
    id: int,
    data: Account,
    _: str = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> Account:
    return await view.update_account(
        id,
        data,
    )


@account_router.delete(
    "/account/{id}",
)
async def delete_account(
    id: int,
    _: str = Depends(validate_token),
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
):
    return await view.delete_account(
        id,
    )
