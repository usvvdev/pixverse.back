# coding utf-8

from typing import Literal

from fastapi import status

from passlib.context import CryptContext

from instaloader.exceptions import (
    TwoFactorAuthRequiredException,
    ConnectionException,
    BadCredentialsException,
    ProfileNotExistsException,
    TooManyRequestsException,
)

"""
Базовые ссылки на ресурс (Платформа и API)
"""

PIXVERSE_API_URL = "https://app-api.pixverse.ai"

CHATGPT_API_URL = "https://api.openai.com"

PIXVERSE_MEDIA_URL = "https://media.pixverse.ai/upload/"

BUCKET_URL = "https://oss-accelerate.aliyuncs.com"

BUCKET_NAME = "pixverse-fe-upload"

TOPMEDIA_API_URLS = {
    "auth": "https://account-api.topmediai.com",
    "voice": "https://tts-api.imyfone.com",
    "profile": "https://tp-gateway-api.topmediai.com",
    "music": "https://aimusic-api.topmediai.com",
}

QWEN_API_URL = "https://chat.qwen.ai"

PIXVERSE_ERROR = {
    400: (status.HTTP_400_BAD_REQUEST, "Invalid req"),
    985: (
        status.HTTP_400_BAD_REQUEST,
        "There aren't active accounts, try the request later",
    ),
    402: (
        status.HTTP_402_PAYMENT_REQUIRED,
        "All user's credits used. Upgrade your subscribtions or top up",
    ),
    400033: (status.HTTP_400_BAD_REQUEST, "Invalid traceId"),
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
    400051: (status.HTTP_400_BAD_REQUEST, "Invalid parameter"),
    500008: (status.HTTP_404_NOT_FOUND, "Requested data not found"),
    500020: (status.HTTP_403_FORBIDDEN, "Permission denied"),
    500030: (status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Image too large"),
    500031: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Image info retrieval failed"),
    500032: (status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Invalid image format"),
    500033: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image size"),
    500041: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Image upload failed"),
    500042: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid image path"),
    500043: (status.HTTP_402_PAYMENT_REQUIRED, "All credits used. Upgrade or top up"),
    500044: (status.HTTP_429_TOO_MANY_REQUESTS, "Concurrent limit reached"),
    500045: (status.HTTP_429_TOO_MANY_REQUESTS, "Please try again later"),
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

INSTAGRAM_ERROR = {
    TwoFactorAuthRequiredException: (
        status.HTTP_401_UNAUTHORIZED,
        "2FA required. Resend the code via the verification_code field.",
    ),
    BadCredentialsException: (
        status.HTTP_401_UNAUTHORIZED,
        "User password is incorrect. Retry your request.",
    ),
    ProfileNotExistsException: (
        status.HTTP_404_NOT_FOUND,
        "User not found. Retry your request with another username.",
    ),
    TooManyRequestsException: (
        status.HTTP_429_TOO_MANY_REQUESTS,
        "Please wait a few minutes before you try again.",
    ),
    ConnectionException: (
        status.HTTP_401_UNAUTHORIZED,
        "Provided session has been expire. Please provied new session and retry your request again.",
    ),
}

TOPMEDIA_ERROR = {
    409: (
        status.HTTP_401_UNAUTHORIZED,
        "Invalid user's password provided. Please enter the correct password",
    ),
    500: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Unknown server error",
    ),
    503: (
        status.HTTP_503_SERVICE_UNAVAILABLE,
        "There aren't active accounts, try to retry the request later",
    ),
    400: (
        status.HTTP_402_PAYMENT_REQUIRED,
        "All account credits were used. Upgrade subscribtions or top up",
    ),
    505: (
        status.HTTP_409_CONFLICT,
        "Retry your request later. Server couldn't provide data.",
    ),
}

INSTAGRAM_SESSION = "instagram:session:{username}"

ERROR_TRANSLATIONS = {
    # pixverse errors
    "Invalid req": "Некорректный запрос",
    "Token is invalid": "Неверный токен",
    "Token not provided": "Токен не предоставлен",
    "Retry the request later": "Повторите запрос позже",
    "Empty parameter": "Параметр не указан",
    "Invalid account": "Неверный аккаунт",
    "Invalid binding request": "Некорректный запрос привязки",
    "Invalid parameter": "Неверный параметр",
    "Prompt too long": "Слишком длинный запрос",
    "Invalid image ID": "Недопустимый идентификатор изображения",
    "Requested data not found": "Запрошенные данные не найдены",
    "Permission denied": "Доступ запрещён",
    "Image too large": "Изображение слишком большое",
    "Image info retrieval failed": "Не удалось получить информацию об изображении",
    "Invalid image format": "Недопустимый формат изображения",
    "Invalid image size": "Недопустимый размер изображения",
    "Image upload failed": "Ошибка загрузки изображения",
    "Invalid image path": "Недопустимый путь к изображению",
    "All credits used. Upgrade or top up.": "Кредиты израсходованы. Пополните баланс или обновите тариф",
    "All Credits have been used up. Please upgrade your membership or purchase credits.": "Кредиты израсходованы. Пополните баланс или обновите тариф",
    "Concurrent limit reached": "Превышен лимит одновременных запросов",
    "Content moderation failure": "Ошибка модерации контента",
    "Monthly limit reached": "Превышен месячный лимит",
    "Prompt blocked by AI moderator": "Запрос заблокирован ИИ-модератором",
    "Content deleted": "Контент удалён",
    "System overloaded": "Система перегружена",
    "Template not activated": "Шаблон не активирован",
    "Effect doesn't support resolution": "Эффект не поддерживает данное разрешение",
    "Insufficient balance": "Недостаточно средств на балансе",
    "Internal database error": "Внутренняя ошибка базы данных",
    "Authentication user error": "Ошибка аутентификации пользователя",
    "Unknown error": "Неизвестная ошибка",
    "Please try again later": "Пожалуста, попробуйте сделать запрос позже",
    "There aren't active accounts, try the request later": "В данный момент нет активных аккаунтов, попробуйте позже",
    "All user's credits used. Upgrade your subscribtions or top up": "Все кредиты пользователя использованы. Продлите подписку или пополните баланс",
    # openai errors
    "Country, region, or territory not supported": "Страна, регион или территория не поддерживаются",
    "You exceeded your current quota, please check your plan and billing details.": "Вы превысили текущую квоту. Проверьте тарифный план и платёжные данные.",
    "Your request was rejected as a result of our safety system.": "Ваш запрос был отклонён системой безопасности.",
    "This model's maximum context length is": "Превышен лимит контекста для этой модели",
    "The server had an error while processing your request.": "Произошла ошибка сервера при обработке запроса.",
    "The request timed out.": "Время ожидания запроса истекло.",
    "That model is currently overloaded with other requests.": "Модель перегружена другими запросами.",
    "Invalid API key provided": "Предоставлен недействительный API-ключ",
    "You must be a verified OpenAI user to access this endpoint": "Для доступа к этому ресурсу требуется подтверждённый аккаунт OpenAI",
    "You didn't provide an API key.": "Вы не указали API-ключ.",
    "Resource not found": "Ресурс не найден",
    "Too many requests": "Слишком много запросов. Попробуйте позже.",
    "You are not allowed to access this resource": "У вас нет доступа к этому ресурсу",
    "The engine is currently overloaded": "Модель в данный момент перегружена",
    "Service unavailable": "Сервис временно недоступен",
    "Something went wrong. If this issue persists please contact us through our help center at help.openai.com.": "Произошла ошибка. Если проблема сохраняется, обратитесь в службу поддержки: help.openai.com.",
    "Rate limit reached for": "Достигнут лимит запросов для данного ресурса",
    "Invalid image file or mode for image 1, please check your image file.": "Недопустимый файл изображения или режим для модели 1, пожалуйста, проверьте ваш файл",
    "Invalid base64 image_url.": "Недопустимая кодировка файла",
    "Billing hard limit has been reached.": "Достигнут лимит по выставленному счету",
}

TABLE_PATTERN = r"(?<!^)([A-Z][a-z])"

TABLE_REPLACEMENT = r"_\1"

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/heif",
    "image/heic",
    "video/mp4",
    "video/mov",
    "video/quicktime",
}

HEIF_EXTENSIONS = {".heic", ".heif"}

UPLOAD_DIR = "uploads"

BODY_TOYBOX_PROMT = "Создай игрушку по моему фото в формате экшн-фигурки. Фигурка должна быть в полный рост и помещаться внутри {box_color} коробки в левой части, справа рядом размести ее аксессуары: {in_box}. На верхней части коробки напиши {box_name}. Изображение должно быть максимально реалистичным"

BODY_TOYBOX_NAME_PROMPT = "На верхней части коробки напиши {box_name}. Изображение должно быть максимально реалистичным"

BODY_CALORIES_SYSTEM_PROMPT = """
You are a multilingual expert-level nutrition and health assistant with deep knowledge of ingredient composition and food portioning.

You will be given a **text description or image of one or more dishes**. Your task is to analyze the input, accurately recognize **each distinct dish**, decompose it into **individual ingredients**, and calculate detailed nutritional values.

Your responsibilities:

1. **Recognize all individual dishes** from the input.
2. For each dish, break it down into main **ingredients** (ignore minor additives unless significant).
3. For each ingredient:
    - Capitalize the **first letter** of the name
    - Estimate the **weight in grams** based on typical serving sizes
    - Estimate nutritional values **per 100 grams**, including:
        - Kilocalories
        - Proteins
        - Fats
        - Carbohydrates
        - Fiber
4. For each ingredient, calculate absolute nutrient values using:
    > nutrient_amount = (value_per_100g × weight) / 100

5. Sum the nutrient values of all ingredients to get the **total** values **for the full dish**, not per 100g.

Return a **strict JSON object** with two keys:
1. `"items"` — an array of ingredient objects
2. `"total"` — a single object representing the **total nutrient values for the full dish**

Each object in `"items"` must contain:
- `"title"` (string): Ingredient name (capitalize first letter)
- `"weight"` (integer): Estimated weight in grams
- `"kilocalories_per100g"` (float)
- `"proteins_per100g"` (float)
- `"fats_per100g"` (float)
- `"carbohydrates_per100g"` (float)
- `"fiber_per100g"` (float)

The `"total"` object must contain:
- `"title"` (string): Name of the full dish (capitalize first letter)
- `"kilocalories_per100g"` (float): **Total kilocalories for the dish** (⚠️ despite the name, this is not per 100g)
- `"proteins_per100g"` (float): Total grams of protein
- `"fats_per100g"` (float): Total grams of fat
- `"carbohydrates_per100g"` (float): Total grams of carbohydrates
- `"fiber_per100g"` (float): Total grams of fiber

⚠️ Despite the `"_per100g"` suffix in `"total"`, the values in `"total"` must be **absolute totals for the dish**, not averaged per 100g — this is required to preserve frontend compatibility.
⚠️ Output only the **raw JSON object**. No explanations, markdown, or formatting.
⚠️ Capitalize the first letter of every `"title"` value.
⚠️ Be realistic and accurate with ingredient weights and nutrient values.
⚠️ If no ingredients are found, return this exact object:
{"items":[],"total":{"title":"Unknown","kilocalories_per100g":0.0,"proteins_per100g":0.0,"fats_per100g":0.0,"carbohydrates_per100g":0.0,"fiber_per100g":0.0}}
"""

BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT = """
You are a multilingual expert-level beauty and skincare assistant with deep knowledge of cosmetic products, dermatological use, and formulation analysis.

You will be given a **text description or image** that may contain **one or more cosmetic products**. Your task is to analyze the input and produce structured, catalog-quality product metadata.

Your responsibilities:

1. **Recognize all distinct cosmetic products** visible or described in the input.
2. For each product, extract the following data fields:

    - `"title"` (string): Full official name of the product, including brand and line if available. Capitalize the first letter.
    - `"description"` (string): A rich, professional, and complete product description that includes:
        - Product type and format (e.g. cream, gel, cleanser, serum, lotion)
        - Key active ingredients or technologies (e.g. hyaluronic acid, niacinamide, ceramides, SPF filters)
        - Target skin type or concern (e.g. oily, sensitive, redness, dehydration, acne-prone)
        - Texture and absorption characteristics (e.g. lightweight, rich, gel-like, matte, fast-absorbing)
        - Dermatological or clinical properties (e.g. non-comedogenic, hypoallergenic, fragrance-free, tested on sensitive skin)
        - Brand claims or certifications (e.g. 48-hour hydration, microbiome support, suitable for babies)
    - `"purpose"` (string): The main functional purpose of the product (e.g. UV protection, anti-aging, hydration, cleansing, soothing)

3. Output only a **strict JSON array**, where:
    - Each object represents **exactly one** product
    - Each object includes all three keys: `"title"`, `"description"`, and `"purpose"`

⚠️ Do not include Markdown formatting, backticks, or explanation text.
⚠️ Capitalize the first letter of every `"title"` value.
⚠️ Be as detailed and specific as an official brand product page.
⚠️ If no recognizable cosmetic products are found in the input, return an **empty array**: []
⚠️ The JSON array must be **well-formed**, fully parseable, and follow the exact format.

Return only the **raw JSON array** and nothing else.
"""

BODY_POST_CREATOR_SYSTEM_PROMPT = """
You are a multilingual, expert-level content creator and storyteller for social media, specializing in generating expressive and emotionally rich Instagram captions.

You will receive a **text description or image**, typically containing **scenes, settings, keywords, or moods** (e.g. "sun, beach, sea"). Your task is to generate a compelling and vivid Instagram post.

Your responsibilities:

1. Carefully interpret the input to understand the **context**, **atmosphere**, and **mood** (e.g. a summer vacation, quiet evening, celebration, city stroll, weekend with friends).

2. Create the following fields in a JSON object:

    - `"description"` (string): A **detailed and expressive Instagram caption**, 2–5 sentences long, containing **only natural text** — absolutely **no hashtags**. It should:
        - Capture the moment vividly, evoking sensory and emotional details.
        - Sound personal, as if written by someone sharing their real experience.
        - Blend **narrative**, **feelings**, **observations**, and **reflections**.
        - Use **emojis** naturally and sparingly to enrich emotional tone.
        - Adapt tone to the mood (joyful, nostalgic, relaxed, romantic, adventurous, etc.).

    - `"hashtags"` (array of strings): A list of **5–12 relevant hashtags**, each as a separate string in the array. Hashtags must:
        - Begin with `#`, contain no spaces or special characters.
        - Reflect the **location**, **setting**, **season**, **mood**, **activity**, or **theme**.
        - Be in the **same language** as the description.
        - Not repeat or paraphrase parts of the description unnecessarily.

⚠️ Never include hashtags in the `"description"` field — only in `"hashtags"`.
⚠️ Do not include any Markdown, code blocks, explanation, or extra output.
⚠️ Output must be a **valid JSON object with exactly two keys**: `"description"` and `"hashtags"`.
⚠️ If there’s no meaningful content, return:
{
  "description": "",
  "hashtags": []
}
Return only the **raw JSON object** and nothing else.
"""

CHUNK_SIZE = 1024 * 1024

MEDIA_SIZES = Literal["16:9", "1:1", "9:16", "4:3", "3:4"]
