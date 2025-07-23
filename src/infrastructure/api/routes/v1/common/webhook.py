# coding utf-8

from fastapi import APIRouter, Request

from fastapi.responses import JSONResponse

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
) -> JSONResponse:
    payload = await request.json()

    # event = payload.get("event")
    # user_id = payload.get("user", {}).get("user_id")

    # if event == "subscription_started":
    # ✅ Начисление токенов
    # await add_tokens_to_user(user_id)

    return JSONResponse(
        content={
            "status": IWebhook(
                **payload,
            ).dict
        },
    )
