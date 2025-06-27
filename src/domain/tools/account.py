# coding utf-8

from typing import Any

from ..conf import app_conf

from ..entities.core import IConfEnv

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import (
    PixverseAccountsTokensRepository,
)

from ...interface.schemas.external import (
    UserToken,
)

conf: IConfEnv = app_conf()


token_repository = PixverseAccountsTokensRepository(
    IDatabase(conf),
)


async def update_account_token(
    account: Any,
    token: str,
):
    account_token = await token_repository.fetch_with_filters(
        account_id=account.id,
    )
    body = UserToken(account_id=account.id, jwt_token=token)
    if account_token is not None:
        return await token_repository.update_record(
            account_token.id,
            body,
        )
