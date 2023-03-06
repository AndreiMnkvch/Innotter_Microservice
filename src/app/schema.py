from pydantic import BaseModel

class Item(BaseModel):
    user_id: int
    page_uuid: str
    follower_id: int | None = None
    post_id: int | None = None
    liked_user_id: int | None = None


class PageStatistics(BaseModel):
    page_uuid: str
    posts_count: int
    followers_count: int
    likes_count: int


class UserPagesStatistics(BaseModel):
    user_id: int
    user_stats: list[PageStatistics] | None = None


# {
#   "PK": "USER#user_id",
#   "SK": "PAGE#page_id",
#   "user_id": "user_id",
#   "page_uuid": "page_uuid",
#   "posts": [
#     {
#       "post_id": "post_id",
#       "likes": {1, 2, 4, 6}
#     },
#      {
#       "post_id": "post_id",
#       "likes": {1, 2, 4, 6}
#     },
#   "followers": [
#    1, 2, 4, 6
#       ]
# }
