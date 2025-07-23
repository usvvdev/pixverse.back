# coding utf-8

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
)

from ......domain.tools import add_user_tokens

from ......domain.entities.core import IWebhook


webhook_router = APIRouter(
    tags=["Webhooks"],
)


@webhook_router.post(
    "/webhook",
    status_code=200,
)
async def apphud_webhook(
    request: Request,
) -> IWebhook:
    if request is None:
        raise HTTPException(
            status_code=400,
            detail="Error handling webhook.",
        )

    payload = await request.json()

    data = IWebhook(**payload)

    if data.event.name == "subscription_started":
        await add_user_tokens(
            data.user.user_id,
            data.app.bundle_id,
        )

    return data
