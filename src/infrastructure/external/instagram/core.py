# coding utf-8

from instagrapi import Client

from instagrapi.exceptions import (
    ClientError,
    ChallengeRequired,
    LoginRequired,
)

from redis import Redis

from json import loads, dumps

from pendulum import duration

from ....domain.errors import InstagramError

from ....domain.constants import INSTAGRAM_SESSION


class InstagramCore:
    def __init__(
        self,
        redis: Redis,
        client: Client | None = None,
    ) -> None:
        self._redis = redis
        self._client = client or Client()

    def fetch_user_session(
        self,
        username: str,
    ) -> Client | None:
        key = INSTAGRAM_SESSION.format(
            username=username,
        )
        session = self._redis.get(key)

        if session is not None:
            self._client.set_settings(loads(session))
            try:
                self._client.get_timeline_feed()
                return self._client
            except InstagramError.exceptions as err:
                if isinstance(err, LoginRequired):
                    self._redis.delete(key)
                raise InstagramError.from_exception(err)

        return None

    def save_user_session(
        self,
        username: str,
        client: Client,
    ) -> None:
        key = INSTAGRAM_SESSION.format(
            username=username,
        )
        session_data = dumps(client.get_settings())
        self._redis.set(
            key,
            session_data,
            ex=int(duration(days=30).total_seconds()),
        )
