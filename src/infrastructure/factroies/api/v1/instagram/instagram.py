# coding utf-8

from fastapi import Depends

from redis import Redis

from .....external.instagram import (
    InstagramCore,
    InstagramClient,
)

from ......domain.conf import app_conf

from ......domain.entities.core import IConfEnv

from ......interface.controllers.api.v1 import InstagramController

from .....api.views.v1 import InstagramView


class InstagramClientFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> InstagramClient:
        return InstagramClient(
            InstagramCore(
                # Redis.from_url(
                #     conf.redis_dsn_url,
                #     decode_responses=True,
                # ),
            ),
        )


class InstagramControllerFactory:
    @staticmethod
    def get(
        client: InstagramClient = Depends(
            InstagramClientFactory.get,
        ),
    ) -> InstagramController:
        return InstagramController(
            client,
        )


class InstagramViewFactory:
    @staticmethod
    def create(
        controller: InstagramController = Depends(
            InstagramControllerFactory.get,
        ),
    ) -> InstagramView:
        return InstagramView(
            controller,
        )
