# coding utf-8

from instagrapi import Client

from instagrapi.exceptions import (
    ClientError,
    ChallengeRequired,
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
        self._client: Client = client or Client()

    def fetch_user_session(
        self,
        username: str,
    ) -> Client | None:
        user_session = self._redis.get(
            INSTAGRAM_SESSION.format(
                username=username,
            )
        )
        if not user_session:
            return None

        self._client.set_settings(loads(user_session))
        try:
            self._client.get_timeline_feed()
            return self._client
        except InstagramError.exceptions as err:
            if isinstance(err, ChallengeRequired):
                return None
            raise InstagramError.from_exception(err)

    def save_user_session(
        self,
        username: str,
        client: Client,
    ) -> None:
        user_settings: dict[str] = client.get_settings()
        return self._redis.set(
            INSTAGRAM_SESSION.format(
                username=username,
            ),
            dumps(user_settings),
            ex=int(duration(days=30).total_seconds()),
        )
