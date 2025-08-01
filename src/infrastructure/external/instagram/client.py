# coding utf-8

from typing import Any

from instaloader.instaloader import (
    Instaloader,
    Profile,
)

from fastapi_pagination import (
    Page,
    paginate,
)

from fastapi.concurrency import run_in_threadpool

from .core import InstagramCore

from ....domain.errors import InstagramError

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.repositories import IDatabase

from ....domain.entities.instagram import ISession

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
    IInstagramPost,
)

from ...orm.database.repositories import (
    InstagramUserRepository,
    InstagramSessionRepository,
    InstagramUserPostsRepository,
    InstagramUserRelationsRepository,
)


conf: IConfEnv = app_conf()


user_repository = InstagramUserRepository(
    IDatabase(conf),
)


session_repository = InstagramSessionRepository(
    IDatabase(conf),
)


user_posts_repository = InstagramUserPostsRepository(
    IDatabase(conf),
)


user_relations_repository = InstagramUserRelationsRepository(
    IDatabase(conf),
)


class InstagramClient:
    def __init__(
        self,
        core: InstagramCore,
    ) -> None:
        self._core = core

    # async def __session_loader(
    #     self,
    #     session_data: ISession,
    # ) -> Instaloader:
    #     loader = Instaloader()

    #     loader.context._session.cookies.update(
    #         session_data.dict,
    #     )
    #     return loader

    async def auth_user_session(
        self,
        session_data: ISession,
    ) -> ISession:
        session = await self._core.fetch_user_session(
            session_data,
        )
        return InstagramAuthResponse(
            uuid=session.uuid,
        )

    # async def __fetch_profile(
    #     self,
    #     session_data: ISession,
    #     username: str,
    # ) -> Profile:
    #     try:
    #         loader: Instaloader = await self.__session_loader(session_data)
    #         sleep(uniform(0.5, 1.5))
    #         return Profile.from_username(loader.context, username)
    #     except Exception as err:
    #         raise InstagramError.from_exception(err)

    async def fetch_statistics(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramPost:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        return await user_repository.fetch_one_to_many(
            "id",
            user_session.user_id,
            many=False,
            related=["statistics", "publications"],
        )

    async def fetch_publication(
        self,
        body: IInstagramUser,
        uuid: str,
        id: int,
    ) -> IInstagramPost:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        return await user_posts_repository.fetch_with_filters(
            id=id,
            user_id=user_session.user_id,
        )

    async def fetch_subscribers(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> Page[InstagramFollower]:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        subscribers = await user_relations_repository.fetch_with_filters(
            relation_type="follower",
            user_id=user_session.user_id,
            many=True,
        )

        items: list[InstagramFollower] = list(
            map(
                lambda subscriber: InstagramFollower.model_validate(
                    subscriber,
                ),
                subscribers,
            )
        )

        return paginate(items)

    async def fetch_subscribtions(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str = "mutual",
    ) -> Page[InstagramFollower]:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        subcribtions = await user_relations_repository.fetch_with_filters(
            relation_type=relation_type,
            user_id=user_session.user_id,
            many=True,
        )

        items: list[InstagramFollower] = list(
            map(
                lambda subscribtion: InstagramFollower.model_validate(
                    subscribtion,
                ),
                subcribtions,
            )
        )

        return paginate(items)

    #     session = await self.__auth_user_session(body.session_id)

    #     user: Profile = await self.__fetch_profile(session)

    #     medias: list[Media] = client.user_medias(user.pk, amount=20)

    #     return InstagramUserResponse(
    #         user=InstagramUser.from_user(user),
    #         statistics=InstagramUserStatistics.from_data(
    #             user,
    #             client,
    #             medias,
    #         ),
    #         posts=InstagramPost.from_medias(medias),
    #     )

    # async def fetch_subsribers(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramFollower]:
    #     client: Client | None = await self.__auth_user_session(body)

    #     user: User = self.__fetch_user(
    #         body,
    #         client,
    #     )

    #     try:
    #         subs: dict[str, UserShort] = client.user_followers(
    #             user.pk,
    #         )
    #     except InstagramError.exceptions as err:
    #         raise InstagramError.from_exception(err)

    #     return await self.__fetch_users(subs)

    # async def fetch_subsribtions(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramFollower]:
    #     client: Client | None = await self.__auth_user_session(body)

    #     user: User = self.__fetch_user(
    #         body,
    #         client,
    #     )

    #     try:
    #         subs: dict[str, UserShort] = client.user_following(
    #             user.pk,
    #         )
    #     except InstagramError.exceptions as err:
    #         raise InstagramError.from_exception(err)

    #     return await self.__fetch_users(subs)

    # async def fetch_non_reciprocal_subsribtions(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramFollower]:
    #     client: Client | None = await self.__auth_user_session(body)

    #     user: User = self.__fetch_user(
    #         body,
    #         client,
    #     )

    #     try:

    #         async def call(
    #             client: Client,
    #             user_id: str,
    #         ) -> dict[str, ...]:
    #             followers: dict[str, UserShort] = await run_in_threadpool(
    #                 client.user_followers, user_id
    #             )

    #             following: dict[str, UserShort] = await run_in_threadpool(
    #                 client.user_following, user_id
    #             )

    #             return {
    #                 str(pk): user
    #                 for pk, user in followers.items()
    #                 if pk not in following
    #             }

    #         subs: dict[str, UserShort] = await call(
    #             client,
    #             user.pk,
    #         )

    #     except InstagramError.exceptions as err:
    #         raise InstagramError.from_exception(err)

    #     return await self.__fetch_users(subs)

    # async def fetch_publications(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramPost]:
    #     client: Client | None = await self.__auth_user_session(body)

    #     user: User = self.__fetch_user(
    #         body,
    #         client,
    #     )

    #     try:
    #         medias: list[Media] = client.user_medias(user.pk)
    #     except InstagramError.exceptions as err:
    #         raise InstagramError.from_exception(err)

    #     items: list[InstagramPost] = list(
    #         map(
    #             lambda media: InstagramPost(**media.model_dump()),
    #             medias,
    #         )
    #     )

    #     return paginate(items)
