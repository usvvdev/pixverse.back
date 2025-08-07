# coding utf-8

from ..conf import app_conf

from ..entities.core import IConfEnv

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import (
    PixverseAccountsTokensRepository,
    TopmediaAccountTokenRepository,
)

from ...infrastructure.orm.database.models import (
    PixverseAccountsTokens,
    TopmediaAccountsTokens,
)

from ...interface.schemas.external import (
    UserToken,
)

conf: IConfEnv = app_conf()


pixverse_token_repository = PixverseAccountsTokensRepository(
    IDatabase(conf),
)


topmedia_token_repository = TopmediaAccountTokenRepository(
    IDatabase(conf),
)


tokens_repository: dict[
    str, TopmediaAccountTokenRepository | PixverseAccountsTokensRepository
] = {
    "pixverse": pixverse_token_repository,
    "topmedia": topmedia_token_repository,
}


async def update_account_token(
    account: PixverseAccountsTokens | TopmediaAccountsTokens,
    token: str,
    project: str = "pixverse",
):
    token_repository = tokens_repository.get(project)

    account_token: (
        PixverseAccountsTokens | TopmediaAccountsTokens
    ) = await token_repository.fetch_with_filters(
        account_id=account.id,
    )

    body = UserToken(
        account_id=account.id,
        jwt_token=token,
    )

    if account_token is not None:
        return await token_repository.update_record(
            account_token.id,
            body,
        )
