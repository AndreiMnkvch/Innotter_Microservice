from botocore.errorfactory import ClientError
from boto3.dynamodb.conditions import Key
from .utils import stats_table


async def create_stats_item(user_id: int, page_uuid: str) -> None:

        async with stats_table() as table:

            try:
                await table.put_item(
                    Item={
                        "user_id": user_id,
                        "page_uuid": page_uuid,
                        "posts": []
                    }
                )
            except ClientError:
                raise Exception(
                    "smth gone wrong when creating new item in statistics table")


async def add_page_follower(user_id: int, page_uuid: str, follower_id: int) -> None:

    """updating stats item by appending new follower to followers list"""

    async with stats_table() as table:

        try:
            await table.update_item(
                Key={'user_id': user_id, 'page_uuid': page_uuid},
                UpdateExpression='ADD followers :value',
                ExpressionAttributeValues={':value': {follower_id}}
            )
        except ClientError:
            raise Exception(
                "smth gone wrong when adding new follower to statistics table")


async def delete_item(user_id: int , page_uuid: str) -> None:

    async with stats_table() as table:

        try:
            await table.delete_item(
                Key={
                    'user_id': user_id,
                    'page_uuid': page_uuid
                },
            )
        except ClientError:
            raise Exception(
                "smth gone wrong when deleting related to specific user items in statistics table")


async def delete_all_user_items(user_id: int) -> None:
    async with stats_table() as table:

        try:
            async with table.batch_writer() as batch:
                response = await table.query(
                    KeyConditionExpression=Key('user_id').eq(user_id)
                )
                items = response["Items"]
                print("items:", items)
                for item in items:
                    print('user_id: ', int(item["user_id"]),
                            'page_uuid: ', item["page_uuid"],
                    )
                    await batch.delete_item(
                        Key={
                            'user_id': int(item["user_id"]),
                            'page_uuid': item["page_uuid"]},
                    )
        except ClientError:
            raise Exception(
                "smth gone wrong when deleting related to specific user items in statistics table")

async def add_post(user_id: int, page_uuid: str, post_id: int) -> None:

    async with stats_table() as table:
        try:
            await table.update_item(
                Key={
                    "user_id": user_id,
                    "page_uuid": page_uuid
                },
                UpdateExpression="SET posts = list_append(posts, :value)",

                ExpressionAttributeValues={
                    ':value': [
                            {"post_id": post_id}
                    ]
                }
            )
        except ClientError:
            raise Exception(
                "smth gone wrong when adding new post to the existing item")

async def delete_post(user_id: int, page_uuid: str, post_id: int) -> None:
    async with stats_table() as table:
        try:
            result = await table.get_item(
                Key={
                    "user_id": user_id,
                    "page_uuid": page_uuid
                }
            )
            item = result["Item"]

            print("item:", item)
            if item:
                posts = item["posts"]
                print("posts:", posts)

                for index, post in enumerate(posts):
                    print(index, post)
                    print(type(post["post_id"]), post["post_id"])
                    if int(post["post_id"]) == post_id:
                        return await table.update_item(
                        Key={
                            "user_id": user_id,
                            "page_uuid": page_uuid,
                        },
                        UpdateExpression= f"remove posts[{index}]",
                    )
        except ClientError:
            raise Exception(
                "smth gone wrong when deleting post from the item")



async def add_like(user_id, page_uuid, post_id, liked_user_id):
    async with stats_table() as table:

        try:
            result = await table.get_item(
                Key={
                    "user_id": user_id,
                    "page_uuid": page_uuid
                }
            )
            item = result.get('Item')
            print("item:", item)
            if item:
                posts = item["posts"]
                print("posts:", posts)

                for index, post in enumerate(posts):
                    print(index, post)
                    print(type(post["post_id"]), post["post_id"])
                    if int(post["post_id"]) == post_id:
                        likes = post.get("likes", set())
                        likes.add(liked_user_id)


                        return await table.update_item(
                            Key={
                                "user_id": user_id,
                                "page_uuid": page_uuid,
                            },
                            UpdateExpression= f"SET posts[{index}].likes = :likes",
                            ExpressionAttributeValues={
                                ':likes': likes
                            },
                        )

        except ClientError:
            raise Exception(
                "smth gone wrong when adding new like to the existing item")

async def get_page_stats_db(user_id, page_uuid):
    async with stats_table() as table:
        try:

            result = await table.get_item(
                Key={
                    "user_id": user_id,
                    "page_uuid": page_uuid
                }
            )
            item = result["Item"]
            print("item: ", item)
            followers_set = item.get("followers")
            print("followes set: ", followers_set)
            posts_list = item.get("posts")
            print("posts list: ", posts_list)


            posts_count = len(posts_list) if posts_list is not None else 0
            print("posts count: ", posts_count)
            followers_count = len(followers_set) if followers_set is not None else 0
            print("followers count: ", followers_count)

            likes_count = 0
            for post_map in item.get("posts", []):
                likes_set = post_map.get("likes")
                if likes_set:
                    likes_count += len(likes_set)
            print("likes_count: ", likes_count)
        except ClientError:
            raise Exception(
                "smth gone wrong when deleting related to specific user items in statistics table")
        return {"likes count": likes_count, "posts count": posts_count, "followers_count": followers_count}

async def get_user_stats_db(user_id: int):
    async with stats_table() as table:

        try:
            response = await table.query(
                KeyConditionExpression=Key('user_id').eq(user_id)
            )
            items = response["Items"]
            print("items:", items)
            user_stats = dict()
            for item in items:
                print("item: ", item)
                followers_set = item.get("followers")
                print("followes set: ", followers_set)
                posts_list = item.get("posts")
                print("posts list: ", posts_list)


                posts_count = len(posts_list) if posts_list is not None else 0
                print("posts count: ", posts_count)
                posts_count_temp = user_stats.get("posts_count", 0)
                posts_count_temp += posts_count
                user_stats.update({"posts_count": posts_count_temp})

                followers_count = len(followers_set) if followers_set is not None else 0
                print("followers count: ", followers_count)
                followers_count_temp = user_stats.get("followers_count", 0)
                followers_count_temp += followers_count
                user_stats.update({"followers_count": followers_count_temp})

                likes_count = 0
                for post_map in item.get("posts", []):
                    likes_set = post_map.get("likes")
                    if likes_set:
                        likes_count += len(likes_set)
                print("likes_count: ", likes_count)
                likes_count_temp = user_stats.get("likes_count", 0)
                likes_count_temp += likes_count
                user_stats.update({"likes_count": likes_count_temp})

        except ClientError:
            raise Exception(
                "smth gone wrong when deleting related to specific user items in statistics table")
        return user_stats
