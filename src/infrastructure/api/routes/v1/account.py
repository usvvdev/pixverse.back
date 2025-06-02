# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)

from ...views.v1 import PixverseAccountView

from .....domain.tools import auto_docs

from ....factroies.api.v1 import PixverseAccountViewFactory

from .....interface.schemas.api.account import Account


account_router = APIRouter(tags=["Accounts"])


@account_router.get(
    "/accounts",
)
async def fetch_accounts(
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
):
    return await view.fetch_accounts()


@account_router.get(
    "/account/{id}",
)
async def fetch_account(
    id: int,
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
):
    return await view.fetch_account(
        id,
    )


@account_router.post(
    "/account",
)
async def add_account(
    data: Account,
    view: PixverseAccountView = Depends(PixverseAccountViewFactory.create),
) -> Account:
    return await view.add_account(
        data,
    )
