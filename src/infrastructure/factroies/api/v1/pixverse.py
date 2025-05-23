# coding utf-8

from fastapi import Depends

from ....external.pixverse import (
    PixVerseCore,
    PixVerseClient,
)

from .....interface.controllers.api.v1 import PixVerseController

from ....api.views.v1 import PixVerseView


class PixVerseClientFactory:
    @staticmethod
    def get() -> PixVerseClient:
        return PixVerseClient(
            PixVerseCore(),
        )


class PixVerseControllerFactory:
    @staticmethod
    def get(
        client: PixVerseClient = Depends(
            PixVerseClientFactory.get,
        ),
    ) -> PixVerseController:
        return PixVerseController(
            client,
        )


class PixVerseViewFactory:
    @staticmethod
    def create(
        controller: PixVerseController = Depends(
            PixVerseControllerFactory.get,
        ),
    ) -> PixVerseView:
        return PixVerseView(
            controller,
        )
