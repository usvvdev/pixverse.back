# coding utf-8

from fastapi_pagination import (
    Page,
    paginate,
)

from collections import defaultdict

from asyncio import sleep

from .core import (
    InstagramCore,
    InstagramGPTCore,
)

from ....domain.errors import InstagramError

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.typing.enums import ChatGPTEndpoint

from ....domain.repositories import IDatabase

from ....domain.entities.instagram import (
    ISession,
    InstagramChatGPTBody,
)

from ....interface.schemas.external import (
    IInstagramUser,
    InstagramUser,
    InstagramUserResponse,
    InstagramAuthResponse,
    InstagramUpdateUserResponse,
    InstagramTrackingUserResponse,
    IInstagramUserStatistics,
    InstagramFollower,
    IInstagramPost,
    T2PBody,
    ChatGPTInstagramResponse,
    ChatGPTErrorResponse,
    ChatGPTInstagram,
    ChartData,
)

from ....interface.schemas.api import SearchUser

from ...orm.database.repositories import (
    InstagramUserRepository,
    InstagramSessionRepository,
    InstagramUserPostsRepository,
    InstagramUserRelationsRepository,
    InstagramTrackingRepository,
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

user_tracking_repository = InstagramTrackingRepository(
    IDatabase(conf),
)


class InstagramClient:
    def __init__(
        self,
        core: InstagramCore,
        gpt: InstagramGPTCore,
    ) -> None:
        self._core = core
        self._gpt = gpt

    async def auth_user_session(
        self,
        session_data: ISession,
    ) -> InstagramAuthResponse:
        session = await self._core.fetch_user_session(
            session_data,
        )
        return InstagramAuthResponse(
            uuid=session.uuid,
        )

    async def update_user_data(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramUpdateUserResponse:
        user_data = await self._core.add_user_data(
            uuid,
        )
        return InstagramUpdateUserResponse(
            uuid=uuid,
        )

    async def find_user(
        self,
        uuid: str,
        username: str,
    ) -> SearchUser:
        return await self._core.find_user(
            uuid,
            username,
        )

    async def add_user_tracking(
        self,
        uuid: str,
        user_id: int,
    ) -> InstagramTrackingUserResponse:
        user_data = await self._core.add_user_tracking(
            uuid,
            user_id,
        )
        return InstagramTrackingUserResponse(
            uuid=uuid,
        )

    async def remove_user_tracking(
        self,
        uuid: str,
        user_id: int,
    ) -> bool:
        user_session = await session_repository.fetch_with_filters(
            uuid=uuid,
        )

        if user_session is None:
            raise InstagramError(
                status_code=404,
                detail="User with requested `uuid` is not Found",
            )

        tracking_record = await user_tracking_repository.fetch_with_filters(
            owner_user_id=user_session.user_id,
            target_user_id=user_id,
        )

        return await user_tracking_repository.delete_record(tracking_record.id)

    async def fetch_user_tracking(
        self,
        uuid: str,
    ) -> Page[InstagramUser]:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        tracking_users = await user_tracking_repository.fetch_one_to_many(
            "owner_user_id",
            user_session.user_id,
            related=["target_user_data"],
        )

        items: list[InstagramUser] = list(
            map(
                lambda user: InstagramUser.model_validate(user.target_user_data),
                tracking_users,
            )
        )

        return paginate(items)

    async def fetch_statistics(
        self,
        body: IInstagramUser,
        uuid: str,
    ):
        user_session = await session_repository.fetch_uuid(
            uuid,
        )
        data = await user_repository.fetch_one_to_many(
            "id",
            user_session.user_id,
            many=False,
            related=["statistics", "publications"],
        )

        return InstagramUserResponse(
            **InstagramUser.model_validate(data).dict,
            posts=[IInstagramPost.model_validate(post) for post in data.publications],
            statistics=[
                IInstagramUserStatistics.model_validate(stat)
                for stat in data.statistics
            ],
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

    async def fetch_secret_fans(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str = "secret_fan",
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

    async def image_to_post(
        self,
        uuid: str,
        body: T2PBody,
    ) -> ChatGPTInstagram:
        max_attempts = 10

        last_error = None

        user = await session_repository.fetch_with_filters(uuid=uuid)

        if user is None:
            raise InstagramError(
                status_code=404,
                detail="User with requested `uuid` is not Found",
            )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTInstagramResponse | ChatGPTErrorResponse:
                    return await self._gpt.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=InstagramChatGPTBody.generate_post(
                            body.prompt,
                        ),
                    )

                data: ChatGPTInstagramResponse | ChatGPTErrorResponse = await call(
                    token
                )

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            # return await self.__handle_success(
                            #     body,
                            #     data,
                            # )
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    # return await self.__handle_failure(last_error)
                await sleep(1)
        # return await self.__handle_failure(
        #     last_error,
        #     extra={"Токен авторизации": token},
        # )

    async def user_subscribers_chart(
        self,
        uuid: str,
    ) -> Page[ChartData]:
        user_session = await session_repository.fetch_uuid(
            uuid,
        )

        subscribers = await user_relations_repository.fetch_with_filters(
            relation_type="follower",
            user_id=user_session.user_id,
            many=True,
        )

        date_count = defaultdict(int)

        for s in subscribers:
            created_month = s.created_at.strftime("%Y-%m")
            date_count[created_month] += 1

        items = [
            ChartData(
                month=month,
                count=count,
            )
            for month, count in sorted(date_count.items())
        ]

        return paginate(items)
