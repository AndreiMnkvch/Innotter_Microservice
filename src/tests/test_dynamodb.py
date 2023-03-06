import pytest

from contextlib import contextmanager


@contextmanager
def create_table(dynamodb_client):
    """Create mock DynamoDB table to test full CRUD operations"""

    dynamodb_client.create_table(
        TableName="my-test-table",
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'page_uuid',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'page_uuid',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    yield

class TestDynamoDB:
    """Test CRUD operations on mock DynamoDB table"""

    TABLE_NAME = "my-test-table"

    def test_create_table(self, dynamodb_client):
        """Test creation of 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            res = dynamodb_client.describe_table(TableName=self.TABLE_NAME)
            res2 = dynamodb_client.list_tables()

            assert res['Table']['TableName'] == self.TABLE_NAME
            assert res2['TableNames'] == [self.TABLE_NAME]

    def test_create_stats_item(self, dynamodb_client, user_id: int, page_uuid: str):
            """Test adding an stats item to 'my-test-table' DynamoDB table"""

            with create_table(dynamodb_client):

                add_item = dynamodb_client.put_item(
                    TableName=self.TABLE_NAME,
                    Item={
                        "user_id": {"N": user_id},
                        "page_uuid": {"S": page_uuid},
                    },
                )

                res = dynamodb_client.get_item(
                    TableName=self.TABLE_NAME,
                    Key={
                        "user_id": {"N": user_id},
                        "page_uuid": {"S": page_uuid},
                    },
                )

                assert add_item['ResponseMetadata']['HTTPStatusCode'] == 200
                assert res['Item']['user_id'] == {"N": user_id}
                assert len(res['Item']) == 2

    def test_add_page_follower(self, dynamodb_client, user_id: int, page_uuid: str, follower_id: int):
        """Test updating an item to 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            ## Add an item to update
            dynamodb_client.put_item(
                    TableName=self.TABLE_NAME,
                    Item={
                        "user_id": {"N": user_id},
                        "page_uuid": {"S": page_uuid},
                    },
                )

            ## Update previously added item
            dynamodb_client.update_item(
                TableName=self.TABLE_NAME,
                Key={
                    "user_id": {"N": user_id},
                    "page_uuid": {"S": page_uuid}
                    },
                UpdateExpression='ADD followers :value',
                ExpressionAttributeValues={":value": {"L": [{"S": follower_id}]}}
            )

            res = dynamodb_client.get_item(
                TableName=self.TABLE_NAME,
                Key={
                    "user_id": {"N": user_id}
                },
            )

            assert res['Item']['followers'] == follower_id


