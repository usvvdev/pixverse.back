# coding utf-8

from enum import StrEnum


class InstagramRelationType(StrEnum):
    FOLLOWERS = "followers"
    FOLLOWING = "following"
    SECRET_FANS = "secret_fans"
    NON_RECIPROCAL = "non_reciprocal"
