from contextlib import asynccontextmanager
import aioboto3
import os


@asynccontextmanager
async def stats_table():

    """ manages connection between microservice and dynamodb "Statistics" table """

    session = aioboto3.Session()
    async with session.resource(
        "dynamodb",
        region_name='eu-central-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    ) as dynamodb:
        table = await dynamodb.Table('Statistics')
        yield table
