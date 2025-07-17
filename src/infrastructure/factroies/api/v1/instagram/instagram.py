# coding utf-8

from fastapi import Depends

from redis import Redis

from .....external.instagram import (
    InstagramCore,
    InstagramClient,
)

from ......interface.controllers.api.v1 import InstagramController

from .....api.views.v1 import InstagramView


redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)


class InstagramClientFactory:
    @staticmethod
    def get() -> InstagramClient:
        return InstagramClient(
            InstagramCore(
                redis,
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
