# coding utf-8

from typing import Literal

from .....domain.entities.auth import (
    UserAuthToken,
    RefreshToken,
    AccessToken,
)
from .....domain.jwt import app_auth

from .....infrastructure.orm.database.models import AuthUsers

from .....infrastructure.orm.database.repositories import AuthUserRepository

from .....interface.schemas.api import (
    AuthUserCredentials,
    UserRefreshToken,
)


class AuthUserController:
    def __init__(
        self,
        repository: AuthUserRepository,
    ) -> None:
        self._repository = repository

    async def create_user_tokens(
        self,
        credentials: AuthUserCredentials,
    ) -> UserAuthToken:
        user: AuthUsers | None = await self._repository.fetch_user(
            "username", credentials.username
        )
        if not user or not credentials.validate(user.password):
            raise KeyError
        return app_auth(user, Literal[RefreshToken, AccessToken])

    async def create_access_token(
        self,
        refresh_token: UserRefreshToken,
    ) -> UserAuthToken:
        user: AuthUsers = await self._repository.fetch_user(
            "uuid", refresh_token.validate().uuid
        )
        if not user:
            pass
        return app_auth(user, Literal[AccessToken])
