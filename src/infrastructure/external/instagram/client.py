# coding utf-8

import os

from fastapi import UploadFile

from fastapi_pagination import (
    Page,
    paginate,
)

from base64 import b64encode

from .core import (
    InstagramCore,
    InstagramGPTCore,
)

from ....domain.constants import HEIF_EXTENSIONS

from ....domain.tools import convert_heic_to_jpg

from ....domain.errors import InstagramError

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.repositories import IDatabase

from ....domain.entities.instagram import ISession

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
        # gpt: InstagramGPTCore,
    ) -> None:
        self._core = core
        # self._gpt = gpt

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

    async def image_to_post(
        self,
        image: UploadFile,
    ):
        max_attempts = 10

        last_error = None

        ext = str(os.path.splitext(image.filename)[-1]).lower()
        image_bytes = await image.read()

        if ext in HEIF_EXTENSIONS:
            image_bytes, ext, _ = await convert_heic_to_jpg(
                image_bytes,
            )

        image_base64 = b64encode(image_bytes).decode("utf-8")

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:
                pass
            except:
                pass
