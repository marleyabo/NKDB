from flask import Flask
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table_name = 's3Metadataserverless'
table = dynamodb.Table(table_name)

def search_objects(substring):
    response = table.scan(
        FilterExpression=Attr('Object').contains(substring)
    )

    items = response.get('Items', [])
    object_names = [item['Object'] for item in items]  # Extracting object names
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=Attr('Object').contains(substring),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items = response['Items']
        object_names.extend([item['Object'] for item in items])  # Extracting object names

    return object_names


def get_xls(file_name):
    print("Downloading file:", file_name)

    bucket_name = 'metadatatester'
    local_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', file_name)  # Save file to desktop

    try:
        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Download the file from S3
        with open(local_file_path, 'wb') as f:
            s3.download_fileobj(bucket_name, file_name, f)

        print(f"Successfully downloaded {file_name} from {bucket_name}")
        return local_file_path  # Return the local file path

    except ClientError as e:
        print(f"Failed to download {file_name} from {bucket_name}: {e}")
        return None

def get_video_url_and_start_time(timestamp, results):
    hour, minute = map(int, timestamp.split(':'))
    timestamp_in_seconds = hour * 3600 + minute * 60

    if 9 * 3600 <= timestamp_in_seconds < 12 * 3600:
        video_url = results[0]
        start_time = timestamp_in_seconds - 9 * 3600
    elif 12 * 3600 <= timestamp_in_seconds < 17 * 3600:
        video_url = results[0]
        start_time = timestamp_in_seconds - 12 * 3600
    else:
        video_url = results[0]
        start_time = timestamp_in_seconds - 17 * 3600
    return video_url, start_time
