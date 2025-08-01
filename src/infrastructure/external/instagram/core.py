# coding utf-8

from typing import Iterable

from instaloader.instaloader import (
    Instaloader,
    Profile,
    Post,
    InstaloaderException,
)

from instagrapi import Client

from instagrapi.types import UserShort

from instagrapi.exceptions import ClientLoginRequired, ClientError

from sqlalchemy.exc import DuplicateColumnError

from ....domain.errors import InstagramError

from ....domain.entities.instagram import ISession

from ....interface.schemas.api import (
    Session,
    AddSession,
    IUser,
    User,
)

from ....interface.schemas.external import (
    InstagramUserStatistics,
    InstagramPost,
    InstagramFollower,
)

from requests.cookies import cookiejar_from_dict

from ...orm.database.models import InstagramSessions

from ...orm.database.repositories import (
    InstagramSessionRepository,
    InstagramUserRepository,
    InstagramUserStatsRepository,
    InstagramUserPostsRepository,
    InstagramUserRelationsRepository,
)

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.repositories.engines.database import IDatabase


conf: IConfEnv = app_conf()


session_repository = InstagramSessionRepository(
    IDatabase(conf),
)


user_repository = InstagramUserRepository(
    IDatabase(conf),
)


user_stats_repository = InstagramUserStatsRepository(
    IDatabase(conf),
)


user_posts_repository = InstagramUserPostsRepository(
    IDatabase(conf),
)


user_relations_repository = InstagramUserRelationsRepository(
    IDatabase(conf),
)


class InstagramCore:
    async def __set_loader(
        self,
        session_data: ISession,
    ) -> Instaloader:
        loader = Instaloader()
        try:
            loader.context._session.cookies = cookiejar_from_dict(
                session_data.dict,
                overwrite=True,
            )
        except InstaloaderException as err:
            raise err
        return loader

    async def __set_client(
        self,
        session_data: ISession,
    ) -> Client:
        client = Client()
        try:
            client.login_by_sessionid(session_data.sessionid)
        except ClientLoginRequired as err:
            raise err
        return client

    async def __validate_profile(
        self,
        session_data: ISession,
    ) -> Profile | None:
        loader: Instaloader = await self.__set_loader(session_data)
        try:
            data: Profile | None = Profile.from_id(
                loader.context,
                int(
                    session_data.ds_user_id,
                ),
            )
            return data
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

    async def __iterate_posts(
        self,
        posts: Iterable[Post],
        user_id: int,
    ):
        for post in posts:
            yield InstagramPost.from_instaloader_post(post, user_id)

    async def __add_user_relations(
        self,
        client: Client,
        user_id: int,
    ) -> None:
        try:
            user_info = client.user_info_by_username(client.username)
            user_pk = user_info.pk

            followers: list[UserShort] = client.user_followers(user_pk).values()
            followees: list[UserShort] = client.user_following(user_pk).values()

            follower_usernames = {f.username for f in followers}
            followee_usernames = {f.username for f in followees}

            # 1. follower
            for follower in followers:
                await user_relations_repository.add_record(
                    InstagramFollower.from_instaloader_profile(
                        follower,
                        user_id,
                        relation_type="follower",
                    )
                )

            # 2. following
            for followee in followees:
                await user_relations_repository.add_record(
                    InstagramFollower.from_instaloader_profile(
                        followee,
                        user_id,
                        relation_type="following",
                    )
                )

            # 3. not_following_back — ты не подписан в ответ
            for follower in followers:
                if follower.username not in followee_usernames:
                    await user_relations_repository.add_record(
                        InstagramFollower.from_instaloader_profile(
                            follower,
                            user_id,
                            relation_type="not_following_back",
                        )
                    )

            # 4. not_followed_by — они не подписаны на тебя
            for followee in followees:
                if followee.username not in follower_usernames:
                    await user_relations_repository.add_record(
                        InstagramFollower.from_instaloader_profile(
                            followee,
                            user_id,
                            relation_type="not_followed_by",
                        )
                    )

        except ClientError as err:
            raise InstagramError.from_exception(err)

    async def __add_user(
        self,
        session_data: ISession,
    ):
        profile: Profile | None = await self.__validate_profile(
            session_data,
        )
        client = await self.__set_client(session_data)
        if profile is not None:
            user_data = IUser.from_instaloader_profile(
                profile,
            )

            if (
                await user_repository.fetch_field("username", profile.username, False)
                is None
            ):
                await user_repository.add_record(
                    user_data,
                )

            user = await user_repository.fetch_field(
                "username",
                user_data.username,
                False,
            )

            user_stats = InstagramUserStatistics.from_instaloader_profile(
                profile,
                user.id,
            )

            if (
                await user_stats_repository.fetch_field("user_id", user.id, False)
                is None
            ):
                await user_stats_repository.add_record(
                    user_stats,
                )

            posts = profile.get_posts()

            if (
                await user_posts_repository.fetch_field("user_id", user.id, False)
                is None
            ):
                async for post in self.__iterate_posts(posts, user.id):
                    await user_posts_repository.add_record(post)

            await self.__add_user_relations(client, user.id)

            return AddSession(
                **session_data.dict,
                user_id=user.id,
            )

    async def fetch_user_session(
        self,
        session_data: ISession,
    ) -> InstagramSessions:
        session: InstagramSessions | None = await session_repository.fetch_session(
            session_data.sessionid,
        )
        if session is not None:
            return session
        return await self.save_user_session(
            session_data,
        )

    async def save_user_session(
        self,
        session_data: ISession,
    ) -> ISession:
        try:
            await session_repository.add_record(
                await self.__add_user(session_data),
            )
        except DuplicateColumnError as err:
            raise err

        return await session_repository.fetch_session(
            session_data.sessionid,
        )
