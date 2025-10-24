import os
import boto3
from botocore.config import Config

TABLE = os.getenv("DYNAMO_TABLE_NAME", "conversation")
REGION = os.getenv("AWS_REGION", "us-east-1")
LOCALSTACK_URL = os.getenv("LOCALSTACK_URL", "http://0.0.0.0:4566")

# AWS Connection
_session = boto3.session.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRETS_ACCESS_KEY", "test"),
    region_name=REGION
)

# Dynamo DB connection
_dynamo = _session.resource(
    "dynamodb",
    endpoint_url=LOCALSTACK_URL,
    config=Config(retries={"max_attempts": 3})
)


def ensure_table():
    existing = [t.name for t in _dynamo.tables.all()] # python list compression
    if TABLE in existing:
        print("Table already present")
        return _dynamo.Table(TABLE)

    # Sharded database - (Multiple system)
    # Consistent Hashing Algo
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
        BillingMode='PAY_PER_REQUEST' # Provisioned
    )


def get_history(conversation_id: str):
    tbl = _dynamo.Table(TABLE)
    resp = tbl.get_item(Key = {"conversation_id": conversation_id})
    return resp.get("Item", {}).get("history", [])


def put_message(conversation_id: str, role: str, content: str):
    tbl = _dynamo.Table(TABLE)
    tbl.update_item(
        Key = {"conversation_id": conversation_id},
        UpdateExpression = "SET #hist = list_append(if_not_exists(#hist, :empty), :msg)",
        ExpressionAttributeNames = {
            "#hist": "history"
        },
        ExpressionAttributeValues = {
            ":empty": [],
            ":msg": [{"role": role, "content": content}]
        },
        ReturnValues="UPDATED_NEW"
    )



"""
Dynamo get_item response payload
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html
{
    'Item': {
        'history': [
            {"role": "user", "content": "What is today weather"},
            {"role": "ai", "content": "Today is sunny looks nice to visit beach" },
            ...,
            .....
        ]
    },
    'ConsumedCapacity': {
        'TableName': 'string',
        'CapacityUnits': 123.0,
        'ReadCapacityUnits': 123.0,
        'WriteCapacityUnits': 123.0,
        'Table': {
            'ReadCapacityUnits': 123.0,
            'WriteCapacityUnits': 123.0,
            'CapacityUnits': 123.0
        },
        'LocalSecondaryIndexes': {
            'string': {
                'ReadCapacityUnits': 123.0,
                'WriteCapacityUnits': 123.0,
                'CapacityUnits': 123.0
            }
        },
        'GlobalSecondaryIndexes': {
            'string': {
                'ReadCapacityUnits': 123.0,
                'WriteCapacityUnits': 123.0,
                'CapacityUnits': 123.0
            }
        }
    }
}
"""
