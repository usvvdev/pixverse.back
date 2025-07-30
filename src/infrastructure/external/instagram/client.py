# coding utf-8

from time import sleep

from random import uniform

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
        def handler(
            username: str,
            choice: int,
        ) -> str:
            if not body.verification_code:
                raise InstagramError.from_exception(TwoFactorRequired)
            return body.verification_code

        return handler

    @staticmethod
    def __generate_settings() -> dict:
        return Client().get_settings()

    def __create_new_client(
        self,
        proxy: str | None = None,
    ) -> Client:
        client = Client()
        if proxy:
            client.set_proxy(proxy)
        client.set_settings(self.__generate_settings())
        return client

    async def __auth_user_session(
        self,
        body: IInstagramUser,
    ) -> Client:
        try:
            client: Client | None = self._core.fetch_user_session(
                body.username,
            )
            if client:
                return client
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        raise InstagramError.from_exception(LoginRequired)

    def __fetch_user(
        self,
        body: IInstagramUser,
        client: Client,
    ) -> User:
        try:
            sleep(uniform(0.5, 1.5))
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
        print(body)

        if _ := self._core.fetch_user_session(body.username):
            return InstagramSessionResponse(
                username=body.username,
            )

        client: Client = self.__create_new_client(
            proxy="http://k0XRJ4:A1GETc@196.17.251.251:8000",
        )
        client.challenge_code_handler = self.__handle_code(
            body.verification_code,
        )

        try:
            if body.verification_code:
                client.login(
                    **body.model_dump(exclude=body.exclude_fields()),
                )
            else:
                client.login(body.username, body.password)
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        self._core.save_user_session(
            body.username,
            client,
        )
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
