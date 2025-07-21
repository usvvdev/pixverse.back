# coding utf-8

from instagrapi import Client

from fastapi import HTTPException

from fastapi_pagination import (
    Page,
    paginate,
)

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

    async def user_auth(
        self,
        body: InstagramAuthUser,
    ) -> InstagramSessionResponse | InstagramAuthResponse:
        if _ := self._core.fetch_user_session(body.username):
            return InstagramSessionResponse(
                username=body.username,
            )

        client = Client()

        def code_handler(
            username: str,
            choice,
        ) -> str:
            if not body.verification_code:
                raise HTTPException(
                    status_code=401,
                    detail="Verification code required. Provide it in 'verification_code'.",
                )
            return body.verification_code

        client.challenge_code_handler = code_handler

        try:
            if not body.verification_code:
                client.login(body.username, body.password)
            client.login(
                **body.model_dump(
                    exclude={"user_id", "app_id"},
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

        if client is not None:
            try:
                user: User = client.user_info_by_username(
                    body.username if search_user is None else search_user
                )
            except InstagramError.exceptions as err:
                raise InstagramError.from_exception(err)

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

    async def fetch_users(
        self,
        body: IInstagramUser,
        type: InstagramRelationType,
        search_user: str | None = None,
    ) -> Page[InstagramFollower]:
        async def call(username: str) -> Client | None:
            return self._core.fetch_user_session(username=username)

        try:
            client = await call(body.username)
        except Exception:
            try:
                client = await call(body.username)
            except InstagramError.exceptions as err:
                raise InstagramError.from_exception(err)

        if client is None:
            return paginate([])
        try:
            user_id = (
                client.user_id
                if not search_user
                else client.user_info_by_username(search_user).pk
            )

            followers = lambda: client.user_followers(user_id)
            following = lambda: client.user_following(user_id)

            def secret_fans():
                f = followers()
                g = following()
                return {pk: f[pk] for pk in set(f) - set(g)}

            def non_reciprocal():
                f = followers()
                g = following()
                return {pk: g[pk] for pk in set(g) - set(f)}

            fetch_map: dict[InstagramRelationType, ...] = {
                InstagramRelationType.FOLLOWERS: followers,
                InstagramRelationType.FOLLOWING: following,
                InstagramRelationType.SECRET_FANS: secret_fans,
                InstagramRelationType.NON_RECIPROCAL: non_reciprocal,
            }

            if type not in fetch_map:
                raise ValueError(f"Unsupported type: {type}")

            subs: dict[str, UserShort] = fetch_map[type]()

        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

        items: list[InstagramFollower] = list(
            map(
                lambda sub: InstagramFollower(
                    **sub.model_dump(),
                ),
                subs.values(),
            )
        )

        return paginate(items)
