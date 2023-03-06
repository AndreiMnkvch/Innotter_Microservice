import json
from .schema import Item
from aio_pika import connect, ExchangeType
from .dynamodb.db import (
    create_stats_item,
    add_page_follower,
    delete_all_user_items,
    delete_item,
    add_post,
    add_like,
    delete_post
)


async def on_message(message) -> None:
    match message.routing_key:
        case "users.delete":
            data = json.loads(message.body.decode("utf-8"))
            user_id = data["user_id"]
            await delete_all_user_items(user_id)

        case "pages.create":
            data = json.loads(message.body.decode("utf-8"))
            item = Item(**data)
            await create_stats_item(item.user_id, item.page_uuid)

        case "pages.update":
            data = json.loads(message.body.decode("utf-8"))
            item = Item(**data)
            await add_page_follower(item.user_id, item.page_uuid, item.follower_id)

        case "pages.delete":
            data = json.loads(message.body.decode("utf-8"))
            item = Item(**data)
            await delete_item(item.user_id, item.page_uuid)

        case "posts.create":
            data = json.loads(message.body.decode("utf-8"))
            item = Item(**data)
            await add_post(item.user_id, item.page_uuid, item.post_id)

        case "posts.liked":
            data = json.loads(message.body.decode("utf-8"))
            item = Item(**data)
            await add_like(item.user_id, item.page_uuid, item.post_id, item.liked_user_id)

        case "posts.delete":
            data = json.loads(message.body.decode("utf-8"))
            item = Item(**data)
            await delete_post(item.user_id, item.page_uuid, item.post_id)


async def consume(loop) -> None:

    connection = await connect(
        "amqp://rabbitmq:rabbitmq@rabbitmq:5672",
         loop=loop
    )


    channel = await connection.channel()

    topic_exchange = await channel.declare_exchange(
        "topic",
        type=ExchangeType.TOPIC,
        durable=True,
    )

    queue = await channel.declare_queue("statistics", durable=True)

    binding_keys = [
        "pages.update",
        "users.create",
        "users.delete",
        "pages.create",
        "pages.delete",
        "posts.create",
        "posts.delete",
        "posts.liked"
        ]
    for binding_key in binding_keys:
        await queue.bind(exchange=topic_exchange, routing_key=binding_key)

    await queue.consume(on_message)
