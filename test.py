# from src.infrastructure.orm.database.models.instagram.session import InstagramSessions
# from src.infrastructure.external.instagram.core import InstagramCore

# from src.domain.entities.instagram import ISession


# from asyncio import run


# core = InstagramCore()


# session = {
#     "csrftoken": "4BktVNlJernkPP0iN6dnciASlDx5LDgX",
#     "ds_user_id": "4241541665",
#     "sessionid": "4241541665%3AQjXGsICyxPXaX9%3A27%3AAYeEKNVGEoT9B14kQtw26WZwPKS1B20mV-mGXbMneQ",
# }

# session_data = ISession(**session)


# async def main():
#     session: InstagramSessions = await core.fetch_user_session(session_data)
#     return session.uuid


# print(run(main()))


# import requests
# from requests.cookies import cookiejar_from_dict
# from instagrapi import Client


# def create_client_with_requests_session(cookies: dict) -> Client:
#     # Создаем сессию requests
#     session = requests.Session()
#     # Устанавливаем куки с правильным доменом и путем
#     jar = cookiejar_from_dict(cookies)
#     session.cookies.update(jar)

#     # Создаем instagrapi клиент с нашей сессией
#     client = Client(requests_session=session)

#     # Проверим авторизацию: например, загрузим профиль по user_id
#     user_id = int(cookies["ds_user_id"])
#     profile = client.user_info(user_id)
#     print(f"Logged in as: {profile.username}")

#     return client


# if __name__ == "__main__":
#     session_cookies = {
#         "csrftoken": "4BktVNlJernkPP0iN6dnciASlDx5LDgX",
#         "ds_user_id": "4241541665",
#         "sessionid": "4241541665%3AB8Qah8r9WHq1xr%3A8%3AAYchcJvHJpT-No2l6yQBINdRzvHjGvO6UNddXHyYNA",
#     }
#     client = create_client_with_requests_session(session_cookies)
#     user_id = int(session_cookies["ds_user_id"])
#     profile = client.user_info(user_id)
#     print(profile)


from instagrapi import Client
from requests.cookies import cookiejar_from_dict


def create_client_with_cookies(cookies: dict) -> Client:
    client = Client()
    # Вставляем куки напрямую в сессию requests
    client.login_by_sessionid(cookies.get("sessionid"))
    return client


if __name__ == "__main__":
    cookies = {
        "csrftoken": "4BktVNlJernkPP0iN6dnciASlDx5LDgX",
        "ds_user_id": "4241541665",
        "sessionid": "4241541665%3AB8Qah8r9WHq1xr%3A8%3AAYchcJvHJpT-No2l6yQBINdRzvHjGvO6UNddXHyYNA",
    }

    client = create_client_with_cookies(cookies)

    user_id = int(cookies["ds_user_id"])
    profile = client.user_info(user_id)
    print(profile)
