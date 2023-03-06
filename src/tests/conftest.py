import boto3
import os
import pytest
import uuid

from moto import mock_dynamodb


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb_client(aws_credentials):
    """DynamoDB mock client."""
    with mock_dynamodb():
        conn = boto3.client("dynamodb", region_name="us-east-1")
        yield conn

@pytest.fixture
def user_id():
    return "1"

@pytest.fixture
def page_uuid():
    return str(uuid.uuid4())

@pytest.fixture
def follower_id():
    return "2"
