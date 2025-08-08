# coding utf-8

from httpx import HTTPError

from fastapi import HTTPException

from typing import (
    Any,
    Generator,
    Iterable,
)

from instaloader.instaloader import (
    Instaloader,
    Profile,
    Post,
    InstaloaderException,
)

from pendulum import now

from instagrapi import Client

from instagrapi.types import UserShort

from instagrapi.exceptions import (
    ClientLoginRequired,
    ClientError,
)

from sqlalchemy.exc import DuplicateColumnError

from ....domain.errors import InstagramError

from ....domain.entities.instagram import ISession

from ....interface.schemas.api import (
    AddSession,
    IUser,
    SearchUser,
    UserTracking,
)

from ....interface.schemas.external import (
    InstagramUserStatistics,
    InstagramPost,
    InstagramFollower,
    UserRelationStats,
)

from requests.cookies import cookiejar_from_dict

from ...orm.database.models import InstagramSessions

from ...orm.database.repositories import (
    InstagramSessionRepository,
    InstagramUserRepository,
    InstagramUserStatsRepository,
    InstagramUserPostsRepository,
    InstagramUserRelationsRepository,
    InstagramTrackingRepository,
)

from ..core import HttpClient

from ....domain.conf import app_conf

from ....domain.constants import CHATGPT_API_URL

from ....domain.entities.core import IConfEnv

from ....domain.entities.chatgpt import IAuthHeaders

from ....domain.typing.enums import RequestMethod

from ....interface.schemas.external import (
    ChatGPTInstagramResponse,
    ChatGPTErrorResponse,
)

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


user_tracking_repository = InstagramTrackingRepository(
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
        user_id: int | None = None,
    ) -> Profile | None:
        loader: Instaloader = await self.__set_loader(session_data)
        try:
            data: Profile | None = Profile.from_id(
                loader.context,
                int(
                    session_data.ds_user_id if user_id is None else user_id,
                ),
            )
            return data
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

    async def __iterate_posts(
        self,
        posts: Iterable[Post],
        user_id: int,
    ) -> Generator[InstagramPost, Any, None]:
        for post in posts:
            yield InstagramPost.from_instaloader_post(post, user_id)

    def __fetch_relation_stats(
        self,
        followers: list[UserShort],
        followees: list[UserShort],
    ) -> UserRelationStats:
        follower_usernames = {f.username for f in followers}
        followee_usernames = {f.username for f in followees}

        mutual_usernames = follower_usernames & followee_usernames
        not_following_back = follower_usernames - followee_usernames
        not_followed_by = followee_usernames - follower_usernames

        return UserRelationStats(
            follower_usernames,
            followee_usernames,
            mutual_usernames,
            not_following_back,
            not_followed_by,
        )

    async def __add_user_relations(
        self,
        client: Client,
        user_id: int,
    ) -> None:
        try:
            user_info = client.user_info_by_username(client.username)
            user_pk = user_info.pk

            followers = client.user_followers(user_pk).values()
            followees = client.user_following(user_pk).values()

            follower_map = {f.username: f for f in followers}
            followee_map = {f.username: f for f in followees}

            relation_stats = self.__fetch_relation_stats(followers, followees)

            # 1. mutual
            for username in relation_stats.mutual_usernames:
                user = followee_map[username]
                if (
                    await user_relations_repository.fetch_with_filters(
                        user_id=user_id,
                        related_username=user.username,
                        relation_type="mutual",
                    )
                    is None
                ):
                    await user_relations_repository.add_record(
                        InstagramFollower.from_instaloader_profile(
                            user,
                            user_id,
                            relation_type="mutual",
                        )
                    )

            for follower in followers:
                if (
                    await user_relations_repository.fetch_with_filters(
                        user_id=user_id,
                        related_username=follower.username,
                        relation_type="follower",
                    )
                    is None
                ):
                    await user_relations_repository.add_record(
                        InstagramFollower.from_instaloader_profile(
                            follower,
                            user_id,
                            relation_type="follower",
                        )
                    )

            for followee in followees:
                if (
                    await user_relations_repository.fetch_with_filters(
                        user_id=user_id,
                        related_username=followee.username,
                        relation_type="following",
                    )
                    is None
                ):
                    await user_relations_repository.add_record(
                        InstagramFollower.from_instaloader_profile(
                            followee,
                            user_id,
                            relation_type="following",
                        )
                    )

            # 2. not_following_back
            for username in relation_stats.not_following_back:
                user = follower_map[username]
                if (
                    await user_relations_repository.fetch_with_filters(
                        user_id=user_id,
                        related_username=user.username,
                        relation_type="not_following_back",
                    )
                    is None
                ):
                    await user_relations_repository.add_record(
                        InstagramFollower.from_instaloader_profile(
                            user,
                            user_id,
                            relation_type="not_following_back",
                        )
                    )

            # 3. not_followed_by
            for username in relation_stats.not_followed_by:
                user = followee_map[username]
                if (
                    await user_relations_repository.fetch_with_filters(
                        user_id=user_id,
                        related_username=user.username,
                        relation_type="not_following_back",
                    )
                    is None
                ):
                    await user_relations_repository.add_record(
                        InstagramFollower.from_instaloader_profile(
                            user,
                            user_id,
                            relation_type="not_following_back",
                        )
                    )

        except ClientError as err:
            raise InstagramError.from_exception(err)

    async def __fetch_user_data(
        self,
        session_data: ISession,
    ):
        profile: Profile | None = await self.__validate_profile(
            session_data,
        )
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
            return user_data

    async def __add_user_session(
        self,
        session_data: ISession,
    ) -> AddSession:
        user_data = await self.__fetch_user_data(session_data)
        if user_data is not None:
            user = await user_repository.fetch_field(
                "username",
                user_data.username,
                False,
            )
        return AddSession(
            **session_data.dict,
            user_id=user.id,
        )

    async def add_user_data(
        self,
        uuid: str,
    ) -> IUser | None:
        session = await session_repository.fetch_with_filters(
            uuid=uuid,
        )

        session_data = ISession.model_validate(session)

        profile: Profile | None = await self.__validate_profile(
            session_data,
        )

        client = await self.__set_client(session_data)

        user_data = await self.__fetch_user_data(session_data)

        user = await user_repository.fetch_field(
            "username",
            user_data.username,
            False,
        )

        followers = client.user_followers(session_data.ds_user_id).values()

        followees = client.user_following(session_data.ds_user_id).values()

        relation_stats = self.__fetch_relation_stats(followers, followees)

        user_stats = InstagramUserStatistics.from_instaloader_profile(
            profile,
            user.id,
            mutual_count=relation_stats.mutual_count,
            not_following_back_count=relation_stats.not_following_back_count,
            not_followed_by_count=relation_stats.not_followed_by_count,
        )

        if (
            await user_stats_repository.fetch_field("created_at", now().date(), False)
            is None
        ):
            await user_stats_repository.add_record(
                user_stats,
            )

        posts = profile.get_posts()

        if await user_posts_repository.fetch_field("user_id", user.id, False) is None:
            async for post in self.__iterate_posts(posts, user.id):
                if (
                    await user_posts_repository.fetch_with_filters(
                        user_id=user.id,
                        post_url=post.post_url,
                    )
                    is None
                ):
                    await user_posts_repository.add_record(post)

        await self.__add_user_relations(client, user.id)

        return user_data

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
                await self.__add_user_session(session_data),
            )
        except DuplicateColumnError as err:
            raise err

        return await session_repository.fetch_session(
            session_data.sessionid,
        )

    async def find_user(
        self,
        uuid: str,
        username: str,
    ):
        session = await session_repository.fetch_with_filters(
            uuid=uuid,
        )

        session_data = ISession.model_validate(session)

        loader: Instaloader = await self.__set_loader(session_data)
        try:
            data: Profile | None = Profile.from_username(
                loader.context,
                username,
            )
            return SearchUser.model_validate(data)
        except InstagramError.exceptions as err:
            raise InstagramError.from_exception(err)

    async def add_user_tracking(
        self,
        uuid: str,
        user_id: int,
    ) -> None:
        session = await session_repository.fetch_with_filters(
            uuid=uuid,
        )

        session_data = ISession.model_validate(session)

        profile: Profile | None = await self.__validate_profile(
            session_data,
            user_id=user_id,
        )
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

        target_user = await user_repository.fetch_with_filters(
            username=profile.username
        )

        if (
            await user_tracking_repository.fetch_with_filters(
                target_user_id=target_user.id,
                owner_user_id=session.user_id,
            )
            is None
        ):
            await user_tracking_repository.add_record(
                UserTracking(
                    target_user_id=target_user.id,
                    owner_user_id=session.user_id,
                )
            )


class InstagramGPTCore(HttpClient):
    """Базовый клиент для работы с PixVerse API.

    Наследует функциональность Web3 клиента и добавляет специализированные методы
    для взаимодействия с PixVerse API. Автоматически использует базовый URL сервиса.

    Args:
        headers (dict[str, Any]): Заголовки HTTP-запросов (должен содержать JWT)
    """

    def __init__(
        self,
    ) -> None:
        """Инициализация клиента PixVerse.

        Args:
            headers (dict): Заголовки запросов, обязательно включающие:
                - 'Token': Ключ авторизации
        """
        super().__init__(
            CHATGPT_API_URL,  # Базовый URL из конфигурации
        )

    async def post(
        self,
        token: str = None,
        *args,
        **kwargs,
    ) -> ChatGPTInstagramResponse | ChatGPTErrorResponse:
        """Отправка POST-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
                - body (ISchema, optional): Тело запроса
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        try:
            response: dict[str, Any] = await super().send_request(
                RequestMethod.POST,
                headers=IAuthHeaders(
                    token=token,
                )
                if token is not None
                else None,
                timeout=90,
                *args,
                **kwargs,
            )
            print(response)
            if not response.get("error"):
                return ChatGPTInstagramResponse(**response)
            return ChatGPTErrorResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return ChatGPTErrorResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))

    async def get(
        self,
        token: str = None,
        *args,
        **kwargs,
    ) -> ChatGPTInstagramResponse | ChatGPTErrorResponse:
        """Отправка GET-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        try:
            response: dict[str, Any] = await super().send_request(
                RequestMethod.GET,
                headers=IAuthHeaders(
                    token=token,
                )
                if token is not None
                else None,
                timeout=90,
                *args,
                **kwargs,
            )
            if not response.get("error"):
                return ChatGPTInstagramResponse(**response)
            return ChatGPTErrorResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return ChatGPTErrorResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))
