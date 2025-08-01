# coding utf-8

from .user import InstagramUserRepository

from .session import InstagramSessionRepository

from .stats import InstagramUserStatsRepository

from .post import InstagramUserPostsRepository

from .user_relation import InstagramUserRelationsRepository

__all__: list[str] = [
    "InstagramUserRepository",
    "InstagramSessionRepository",
    "InstagramUserStatsRepository",
    "InstagramUserPostsRepository",
    "InstagramUserRelationsRepository",
]
