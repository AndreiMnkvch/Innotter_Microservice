from pydantic import BaseModel

from uuid import UUID


class User(BaseModel):
    user_id: int
    username: str


class Page(BaseModel):
    uuid: UUID
    name: str
    owner: User
    followers: list[User] | None = None


class Post(BaseModel):
    id: int
    page: Page
    likes: list[User] | None = None


class PageStatistics(BaseModel):
    page_uuid: UUID
    posts_count: int
    followers_count: int
    likes_count: int


class UserPagesStatistics(BaseModel):
    user_id: int
    user_stats: list[PageStatistics] | None = None