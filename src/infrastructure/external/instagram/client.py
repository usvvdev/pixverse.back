# coding utf-8

from typing import Callable

from instagrapi import Client

from instagrapi.exceptions import (
    TwoFactorRequired,
    LoginRequired,
)

from fastapi_pagination import (
    Page,
    paginate,
)

from fastapi.concurrency import run_in_threadpool

from instagrapi.types import (
    User,
    Media,
    UserShort,
)

from .core import InstagramCore

from ....domain.errors import InstagramError

from ....domain.typing.enums import InstagramRelationType

from ....interface.schemas.external import (
    IInstagramUser,
    InstagramPost,
    InstagramUser,
    InstagramUserResponse,
    InstagramAuthUser,
    InstagramSessionResponse,
    InstagramAuthResponse,
    InstagramUserStatistics,
    InstagramFollower,
)


class InstagramClient:
    def __init__(
        self,
        core: InstagramCore,
    ) -> None:
        self._core = core

    @staticmethod
    def __handle_code(
        body: InstagramAuthUser,
    ) -> str:
        if not body.verification_code:
            raise InstagramError.from_exception(
                TwoFactorRequired,
            )
        return body.verification_code

    async def __auth_user_session(
        self,
        body: IInstagramUser,
    ) -> Client:
        try:
            client = self._core.fetch_user_session(
                body.username,
            )
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        if client is not None:
            return client

        raise InstagramError.from_exception(
            LoginRequired,
        )

    def __fetch_user(
        self,
        body: IInstagramUser,
        client: Client,
    ) -> User:
        try:
            return client.user_info_by_username(
                body.search_user if body.search_user is not None else body.username
            )
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

    async def __fetch_users(
        self,
        subs: dict[str, UserShort],
    ) -> Page[InstagramFollower]:
        items: list[InstagramFollower] = list(
            map(
                lambda sub: InstagramFollower(
                    **sub.model_dump(),
                ),
                subs.values(),
            )
        )

        return paginate(items)

    async def user_auth(
        self,
        body: InstagramAuthUser,
    ) -> InstagramSessionResponse | InstagramAuthResponse:
        if _ := self._core.fetch_user_session(body.username):
            return InstagramSessionResponse(
                username=body.username,
            )

        client = Client()

        client.challenge_code_handler = self.__handle_code(body)

        try:
            if not body.verification_code:
                client.login(body.username, body.password)
            else:
                client.login(
                    **body.model_dump(
                        exclude=body.exclude_fields(),
                    )
                )
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        self._core.save_user_session(body.username, client)

        return InstagramAuthResponse(
            username=body.username,
        )

    async def fetch_statistics(
        self,
        body: IInstagramUser,
    ) -> InstagramUserResponse:
        client: Client | None = await self.__auth_user_session(body)

        user: User = self.__fetch_user(
            body,
            client,
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

    async def fetch_subsribers(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        client: Client | None = await self.__auth_user_session(body)

        user: User = self.__fetch_user(
            body,
            client,
        )

        try:
            subs: dict[str, UserShort] = client.user_followers(
                user.pk,
            )
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        return await self.__fetch_users(subs)

    async def fetch_subsribtions(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        client: Client | None = await self.__auth_user_session(body)

        user: User = self.__fetch_user(
            body,
            client,
        )

        try:
            subs: dict[str, UserShort] = client.user_following(
                user.pk,
            )
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        return await self.__fetch_users(subs)

    async def fetch_non_reciprocal_subsribtions(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        client: Client | None = await self.__auth_user_session(body)

        user: User = self.__fetch_user(
            body,
            client,
        )

        try:

            async def call(
                client: Client,
                user_id: str,
            ) -> dict[str, ...]:
                followers: dict[str, UserShort] = await run_in_threadpool(
                    client.user_followers, user_id
                )

                following: dict[str, UserShort] = await run_in_threadpool(
                    client.user_following, user_id
                )

                return {
                    str(pk): user
                    for pk, user in followers.items()
                    if pk not in following
                }

            subs: dict[str, UserShort] = await call(
                client,
                user.pk,
            )

        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        return await self.__fetch_users(subs)

    async def fetch_publications(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramPost]:
        client: Client | None = await self.__auth_user_session(body)

        user: User = self.__fetch_user(
            body,
            client,
        )

        try:
            medias: list[Media] = client.user_medias(user.pk)
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        items: list[InstagramPost] = list(
            map(
                lambda media: InstagramPost(**media.model_dump()),
                medias,
            )
        )

        return paginate(items)
