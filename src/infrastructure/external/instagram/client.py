# coding utf-8

from instagrapi import Client

from instagrapi.types import (
    User,
    Media,
)

from .core import InstagramCore

from ....domain.errors import InstagramError

from ....interface.schemas.external import (
    IInstagramUser,
    InstagramPost,
    InstagramUser,
    InstagramUserResponse,
    InstagramAuthUser,
    InstagramSessionResponse,
    InstagramAuthResponse,
    InstagramUserStatistics,
)


class InstagramClient:
    def __init__(
        self,
        core: InstagramCore,
    ) -> None:
        self._core = core

    async def user_auth(
        self,
        body: InstagramAuthUser,
    ) -> InstagramSessionResponse | InstagramAuthResponse:
        if _ := self._core.fetch_user_session(body.username):
            return InstagramSessionResponse(
                username=body.username,
            )

        client = Client()
        try:
            if not body.verification_code:
                client.login(body.username, body.password)
            client.login(
                **body.model_dump(
                    exclude={"userId", "appId"},
                )
            )
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        self._core.save_user_session(body.username, client)

        return InstagramAuthResponse(
            username=body.username,
        )

    async def fetch_user_statistics(
        self,
        body: IInstagramUser,
        search_user: str | None = None,
    ) -> InstagramUserResponse:
        # max_attempts = 10

        # for attempt in range(max_attempts):
        try:

            async def call(
                usernmame: str,
            ) -> Client | None:
                return self._core.fetch_user_session(
                    username=usernmame,
                )

            client = await call(body.username)
        except Exception:
            # if attempt == max_attempts - 1:
            try:
                client = await call(body.username)
            except InstagramError.exceptions as err:
                raise InstagramError.from_exception(err)

        user: User = client.user_info_by_username(
            body.username if search_user is None else search_user
        )

        medias: list[Media] = client.user_medias(user.pk, amount=20)

        return InstagramUserResponse(
            user=InstagramUser.from_user(user),
            statistics=InstagramUserStatistics.from_data(
                user,
                client,
                medias,
            ),
            posts=InstagramPost.from_medias(medias),
        )
