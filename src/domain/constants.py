# coding utf-8

from fastapi import status

from passlib.context import CryptContext

"""
Базовые ссылки на ресурс (Платформа и API)
"""

PIXVERSE_API_URL = "https://app-api.pixverse.ai"

CHATGPT_API_URL = "https://api.openai.com"

PIXVERSE_MEDIA_URL = "https://media.pixverse.ai/upload/"

BUCKET_URL = "https://oss-accelerate.aliyuncs.com"

BUCKET_NAME = "pixverse-fe-upload"

PIXVERSE_ERROR = {
    400: (status.HTTP_400_BAD_REQUEST, "Invalid req"),
    10001: (status.HTTP_401_UNAUTHORIZED, "Token is invalid"),
    10003: (status.HTTP_403_FORBIDDEN, "Token not provided"),
    10005: (status.HTTP_401_UNAUTHORIZED, "Invalid token provided"),
    400011: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Empty parameter"),
    400012: (status.HTTP_401_UNAUTHORIZED, "Invalid account"),
    400013: (status.HTTP_400_BAD_REQUEST, "Invalid binding request"),
    400017: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid parameter"),
    400018: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Prompt too long"),
    400019: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Prompt too long"),
    400032: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image ID"),
    500008: (status.HTTP_404_NOT_FOUND, "Requested data not found"),
    500020: (status.HTTP_403_FORBIDDEN, "Permission denied"),
    500030: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Image too large"),
    500031: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Image info retrieval failed"),
    500032: (status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Invalid image format"),
    500033: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image size"),
    500041: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Image upload failed"),
    500042: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image path"),
    500043: (status.HTTP_402_PAYMENT_REQUIRED, "All credits used. Upgrade or top up."),
    500044: (status.HTTP_429_TOO_MANY_REQUESTS, "Concurrent limit reached"),
    500054: (status.HTTP_403_FORBIDDEN, "Content moderation failure"),
    500060: (status.HTTP_429_TOO_MANY_REQUESTS, "Monthly limit reached"),
    500063: (status.HTTP_403_FORBIDDEN, "Prompt blocked by AI moderator"),
    500064: (status.HTTP_404_NOT_FOUND, "Content deleted"),
    500069: (status.HTTP_503_SERVICE_UNAVAILABLE, "System overloaded"),
    500070: (status.HTTP_400_BAD_REQUEST, "Template not activated"),
    500071: (status.HTTP_400_BAD_REQUEST, "Effect doesn't support resolution"),
    500090: (status.HTTP_402_PAYMENT_REQUIRED, "Insufficient balance"),
    500100: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal database error"),
    500201: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Authentication user error"),
    99999: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Unknown error"),
}

TABLE_PATTERN = r"(?<!^)([A-Z][a-z])"

TABLE_REPLACEMENT = r"_\1"

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "video/mp4",
    "video/mov",
    "video/quicktime",
}

UPLOAD_DIR = "uploads"

BODY_TOYBOX_PROMT = "Создай игрушку по моему фото в формате экшн-фигурки. Фигурка должна быть в полный рост и помещаться внутри {box_color} коробки в левой части, справа рядом размести ее аксессуары: {in_box}. На верхней части коробки напиши {box_name}. Изображение должно быть максимально реалистичным"

BODY_TOYBOX_NAME_PROMPT = "На верхней части коробки напиши {box_name}. Изображение должно быть максимально реалистичным"

BODY_CALORIES_SYSTEM_PROMPT = """
You are a top-tier nutrition and health assistant. Analyze the provided food input (text or image) and return only a strict JSON array.

Each array element must include:
- "title" (string): Name of the food item
- "weight" (integer): Estimated weight in grams
- "kilocalories_per100g" (float)
- "proteins_per100g" (float)
- "fats_per100g" (float)
- "carbohydrates_per100g" (float)
- "fiber_per100g" (float)

⚠️ Output ONLY the JSON array. No explanations, markdown, or additional text.
⚠️ If no food is detected, return an empty array: []

Example:
[
  {
    "title": "Sushi Rice",
    "weight": 100,
    "kilocalories_per100g": 130,
    "proteins_per100g": 2.5,
    "fats_per100g": 0.2,
    "carbohydrates_per100g": 28.7,
    "fiber_per100g": 0.5
  }
]
"""
