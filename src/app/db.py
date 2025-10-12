import os
import boto3
from botocore.config import Config

TABLE = os.getenv("DYNAMO_TABLE_NAME", "conversation")
REGION = os.getenv("AWS_REGION", "us-east-1")
LOCALSTACK_URL = os.getenv("LOCALSTACK_URL", "http://0.0.0.0:4566")

_session = boto3.session.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRETS_ACCESS_KEY", "test"),
    region_name=REGION
)

_dynamo = _session.resource(
    "dynamodb",
    endpoint_url=LOCALSTACK_URL,
    config=Config(retries={"max_attempts": 3})
)


def ensure_table():
    existing = [t.name for t in _dynamo.tables.all()] # list compression
    if TABLE in existing:
        print("Table already present")
        return _dynamo.Table(TABLE)

    _dynamo.create_table(
        TableName = TABLE,
        KeySchema= [
            {
                'AttributeName': 'conversation_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'conversation_id',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )


