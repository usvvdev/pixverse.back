# coding utf-8

from typing import (
    Annotated,
    Union,
)

from pydantic import Field

from ..core import ISchema

from ...constants import (
    BODY_CALORIES_SYSTEM_PROMPT,
    BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT,
)


class IBody(ISchema):
    """Базовое тело запроса для конфигурации AI-модели.

    Содержит обязательные параметры для работы с AI-моделью:
    - Выбор конкретной модели
    - Длительность обработки
    - Текст запроса (промпт)
    - Качество результата

    Наследует все особенности сериализации от ISchema.
    """

    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    prompt: Annotated[
        str,
        Field(...),
    ]


class PhotoBody(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    model: Annotated[
        str,
        Field(default="gpt-image-1"),
    ]
    size: Annotated[
        str,
        Field(default="auto"),
    ]


class I2CBody(ISchema):
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="appId"),
    ]


class T2CBody(I2CBody):
    description: Annotated[
        str,
        Field(...),
    ]


class T2PBody(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    id: Annotated[
        int,
        Field(...),
    ]


class TB2PBody(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    box_name: Annotated[
        str,
        Field(...),
    ]
    id: Annotated[
        int | None,
        Field(default=None),
    ]
    box_color: Annotated[
        str | None,
        Field(default=None),
    ]
    in_box: Annotated[
        str | None,
        Field(default=None),
    ]


class IImageUrl(ISchema):
    url: Annotated[
        str,
        Field(...),
    ]


class IImageContent(ISchema):
    type: Annotated[
        str,
        Field(default="image_url"),
    ]
    image_url: Annotated[
        IImageUrl,
        Field(...),
    ]


class ITextContent(ISchema):
    type: Annotated[
        str,
        Field(default="text"),
    ]
    text: Annotated[
        str,
        Field(...),
    ]


class IMessage(ISchema):
    role: Annotated[
        str,
        Field(...),
    ]
    content: list[Union[str, ITextContent, IImageContent]]


class CaloriesBody(ISchema):
    model: Annotated[
        str,
        Field(default="gpt-4o"),
    ]
    temperature: Annotated[
        int,
        Field(default=0),
    ]
    top_p: Annotated[
        int,
        Field(default=1),
    ]
    frequency_penalty: Annotated[
        int,
        Field(default=0),
    ]
    presence_penalty: Annotated[
        int,
        Field(default=0),
    ]
    messages: list[IMessage]

    @classmethod
    def create_text(cls, description: str) -> "CaloriesBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_CALORIES_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[ITextContent(text=f"Analyze this food: {description}")],
                ),
            ],
        )

    @classmethod
    def create_image(cls, image_url: str) -> "CaloriesBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_CALORIES_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(text="Analyze the food in this image."),
                        IImageContent(image_url=IImageUrl(url=image_url)),
                    ],
                ),
            ],
        )


class CosmeticBody(ISchema):
    model: Annotated[
        str,
        Field(default="gpt-4o"),
    ]
    temperature: Annotated[
        int,
        Field(default=0),
    ]
    top_p: Annotated[
        int,
        Field(default=1),
    ]
    frequency_penalty: Annotated[
        int,
        Field(default=0),
    ]
    presence_penalty: Annotated[
        int,
        Field(default=0),
    ]
    messages: list[IMessage]

    @classmethod
    def create_text(cls, description: str) -> "CosmeticBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(
                            text=f"Analyze the following cosmetic products: {description}"
                        )
                    ],
                ),
            ],
        )

    @classmethod
    def create_image(cls, image_url: str) -> "CosmeticBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(
                            text="Please identify and list all visible cosmetic products in this photo. Include brand names, product types, and packaging characteristics if possible."
                        ),
                        IImageContent(image_url=IImageUrl(url=image_url)),
                    ],
                ),
            ],
        )
