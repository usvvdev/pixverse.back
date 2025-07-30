# coding utf-8

from ......infrastructure.orm.database.repositories import (
    ApplicationRepository,
    WebhookRepository,
)

from ......interface.schemas.api import (
    StoreApplication,
    ChangeStoreApplication,
    AddStoreApplication,
    Webhook,
)

from ......domain.entities.core import IConfEnv

from ......domain.repositories.engines import IDatabase

from ......domain.conf import app_conf


conf: IConfEnv = app_conf()


webhook_repository = WebhookRepository(
    IDatabase(
        conf,
    )
)


class ApplicationController:
    def __init__(
        self,
        repository: ApplicationRepository,
    ) -> None:
        self._repository = repository

    async def fetch_applications(
        self,
    ) -> list[StoreApplication]:
        return await self._repository.fetch_all(
            ["products"],
        )

    async def fetch_application(
        self,
        id: int,
    ) -> StoreApplication:
        return await self._repository.fetch_application(
            "id",
            id,
        )

    async def add_application(
        self,
        data: AddStoreApplication,
    ) -> AddStoreApplication:
        webhooks = await webhook_repository.fetch_all()

        valid_app_ids = {webhook.app_id for webhook in webhooks}
        if data.application_id not in valid_app_ids:
            await webhook_repository.add_record(
                Webhook(app_id=data.application_id),
            )

        fetched_webhook = await webhook_repository.fetch_with_filters(
            app_id=data.application_id
        )

        return await self._repository.add_record(
            AddStoreApplication(
                **data.dict,
                webhook_url=fetched_webhook.uuid,
            )
        )

    async def delete_application(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeStoreApplication,
    ) -> ChangeStoreApplication:
        return await self._repository.update_record(
            id,
            data,
        )
