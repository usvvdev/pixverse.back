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
    10005: (status.HTTP_409_CONFLICT, "Retry the request later"),
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
You are a multilingual expert-level nutrition and health assistant. Analyze the provided input — a photo or text description — and decompose each recognized dish into its **ingredients**.

Your task:
- Identify all main ingredients of the dish
- Capitalize the first letter of each ingredient's name
- Estimate the weight (in grams) of each ingredient
- Estimate nutritional values per 100 grams for each ingredient
- Calculate the total weight and total nutrients of the full dish
- Finally, calculate the average nutritional values **per 100 grams of the entire dish** using the formula:
  > average_per100g = (total_nutrient / total_weight) × 100

Return a **strict JSON object** with two keys:
1. `"items"` — an array of ingredient objects
2. `"total"` — a single object representing the total nutritional values **per 100 grams of the entire dish**

Each object in `"items"` must contain:
- `"title"` (string): Ingredient name (first letter capitalized)
- `"weight"` (integer): Estimated weight in grams
- `"kilocalories_per100g"` (float)
- `"proteins_per100g"` (float)
- `"fats_per100g"` (float)
- `"carbohydrates_per100g"` (float)
- `"fiber_per100g"` (float)

The `"total"` object must contain:
- `"kilocalories_per100g"` (float)
- `"proteins_per100g"` (float)
- `"fats_per100g"` (float)
- `"carbohydrates_per100g"` (float)
- `"fiber_per100g"` (float)

⚠️ Output only the **raw JSON object**. No explanations, markdown, text, or formatting.
⚠️ Capitalize the first letter of every `"title"` value.
⚠️ If no ingredients are found, return this exact object:
{"items":[],"total":{"kilocalories_per100g":0.0,"proteins_per100g":0.0,"fats_per100g":0.0,"carbohydrates_per100g":0.0,"fiber_per100g":0.0}}
"""
