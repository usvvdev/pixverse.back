# coding utf-8

from fastapi import Depends

from .....domain.conf import app_conf

from .....domain.entities import (
    IConfEnv,
    IHeaders,
)

from ....external.pixverse import (
    PixVerseCore,
    PixVerseClient,
)

from .....interface.controllers.api.v1 import PixVerseController

from ....api.views.v1 import PixVerseView


class PixVerseClientFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(
            app_conf,
        ),
    ) -> PixVerseClient:
        return PixVerseClient(
            PixVerseCore(
                headers=IHeaders(
                    api_key=conf.api_key,
                ).dict,
            ),
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
