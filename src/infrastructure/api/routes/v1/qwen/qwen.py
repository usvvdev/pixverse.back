# coding utf-8

from typing import Any
import requests

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi.responses import JSONResponse

from uuid import uuid4

from pendulum import now

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjZlMjljZDhkLWE4NDktNDZkOS1iMDA0LTgzNjhhYjYwZTYyNSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU0MzkzNzQ2LCJleHAiOjE3NTY5OTMzNTN9.2MOxKOY8xxd8Yj3wMjveSDBxF6Uwe4-0m4Ij0mpMwIw"
}

current_timestamp = int(now().int_timestamp)


qwen_router = APIRouter(tags=["Qwen"])


def create_new_chat(
    headers: dict[str, ...],
):
    request = requests.post(
        "https://chat.qwen.ai/api/v2/chats/new",
        headers=headers,
        json={
            "chat_mode": "normal",
            "chat_type": "t2i",
            "models": ["qwen3-235b-a22b"],
            "timestamp": current_timestamp,
            "title": f"{str(uuid4())}",
        },
    )
    return request.json()


def make_photo(
    headers: dict[str, ...],
    chat_id: str,
    prompt: str,
):
    child_id = str(uuid4())
    request = requests.post(
        f"https://chat.qwen.ai/api/v2/chat/completions?chat_id={chat_id}",
        headers=headers,
        json={
            "stream": False,
            "incremental_output": True,
            "chat_id": f"{chat_id}",
            "chat_mode": "normal",
            "model": "qwen3-235b-a22b",
            "parent_id": None,
            "messages": [
                {
                    "fid": f"{str(uuid4())}",
                    "parentId": None,
                    "childrenIds": [
                        child_id,
                    ],
                    "role": "user",
                    "content": f"{prompt}",
                    "user_action": "chat",
                    "files": [],
                    "timestamp": current_timestamp,
                    "models": ["qwen3-235b-a22b"],
                    "chat_type": "t2i",
                    "feature_config": {
                        "thinking_enabled": False,
                        "output_schema": "phase",
                    },
                    "extra": {"meta": {"subChatType": "t2i"}},
                    "sub_chat_type": "t2i",
                    "parent_id": None,
                }
            ],
            "timestamp": current_timestamp,
            "size": "16:9",
        },
    )
    if request.status_code == 200:
        return child_id


def get_photo(
    headers: dict[str, ...],
    chat_id: str,
):
    request = requests.get(
        f"https://chat.qwen.ai/api/v2/chats/{chat_id}",
        headers=headers,
    )
    res = request.json()

    last_message_id = res["data"]["currentId"]

    return res["data"]["chat"]["history"]["messages"][last_message_id]["content_list"][
        0
    ]["content"]


@qwen_router.post("/text2photo")
async def text_to_photo(
    promptText: str,
) -> JSONResponse:
    new_chat = create_new_chat(headers)

    chat_id = new_chat.get("data").get("id")

    child_id = make_photo(
        headers,
        chat_id,
        promptText,
    )

    if child_id:
        data = get_photo(headers, chat_id)

        return JSONResponse(content={"img_url": data})
