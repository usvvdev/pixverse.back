# coding utf-8

from typing import Annotated

from instaloader import Profile

from pydantic import Field

from uuid import uuid4

from datetime import datetime

from pendulum import now

from ....domain.entities.core import ISchema

from ....domain.entities.instagram import ISession


class AddSession(ISession):
    uuid: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    user_id: Annotated[
        int,
        Field(...),
    ]
    created_at: Annotated[
        datetime,
        Field(default_factory=lambda: now()),
    ]


class Session(AddSession):
    id: Annotated[
        int,
        Field(...),
    ]


class SearchUser(ISchema):
    userid: Annotated[
        int,
        Field(..., alias="user_id"),
    ]
    username: Annotated[
        str,
        Field(...),
    ]
    full_name: Annotated[
        str,
        Field(...),
    ]
    biography: Annotated[
        str,
        Field(...),
    ]
    profile_pic_url: Annotated[
        str | None,
        Field(default=None, alias="profile_picture"),
    ]


class IUser(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    full_name: Annotated[
        str,
        Field(...),
    ]
    biography: Annotated[
        str | None,
        Field(default=None),
    ]
    profile_picture: Annotated[
        str | None,
        Field(default=None),
    ]
    is_private: Annotated[
        bool,
        Field(default=0),
    ]
    is_verified: Annotated[
        bool,
        Field(default=0),
    ]
    is_business_account: Annotated[
        bool,
        Field(default=0),
    ]

    @classmethod
    def from_instaloader_profile(
        cls,
        profile: Profile,
    ) -> "IUser":
        return cls(
            username=profile.username,
            full_name=profile.full_name,
            biography=profile.biography,
            profile_picture=profile.profile_pic_url
            if profile.profile_pic_url
            else None,
            is_private=profile.is_private,
            is_verified=profile.is_verified,
            is_business_account=profile.is_business_account,
        )


class User(IUser):
    id: Annotated[
        int,
        Field(...),
    ]


class UserTracking(ISchema):
    target_user_id: Annotated[
        int,
        Field(...),
    ]
    owner_user_id: Annotated[
        int,
        Field(...),
    ]
    created_at: Annotated[
        datetime,
        Field(default_factory=lambda: now()),
    ]
