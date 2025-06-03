# coding utf-8

from .....interface.controllers.api.v1 import PixverseAccountController

from .....interface.schemas.api import Account


class PixverseAccountView:
    def __init__(
        self,
        controller: PixverseAccountController,
    ) -> None:
        self._controller = controller

    async def fetch_accounts(
        self,
    ) -> list[Account]:
        return await self._controller.fetch_accounts()

    async def fetch_account(
        self,
        id: int,
    ) -> Account:
        return await self._controller.fetch_account(
            id,
        )

    async def add_account(
        self,
        data: Account,
    ) -> Account:
        return await self._controller.add_account(
            data,
        )

    async def update_account(
        self,
        id: int,
        data: Account,
    ) -> Account:
        return await self._controller.update_account(
            id,
            data,
        )

    async def delete_account(
        self,
        id: int,
    ) -> Account:
        return await self._controller.delete_account(
            id,
        )
