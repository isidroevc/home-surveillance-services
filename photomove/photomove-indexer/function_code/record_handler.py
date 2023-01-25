import boto3
from datetime import datetime
import os
def handle_records(records):
    for record in records:
        handle_record(record)

def handle_record(record):
    # deviceId/YYYY_MM_DD/000000000.jpg
    s3 = record['s3']
    object_info = s3['object']
    key = object_info['key']
    key_parts = key.split("/")
    

    if len(key_parts) != 3:
        raise Exception("Object key has not correct path format")
    
    device_id, day_date, file_name = key_parts
    timestamp_string, extension = file_name.split('.')
    timestamp_int = int(timestamp_string)
    if extension != 'jpg':
        raise Exception("Object key has correct extension")
    bucket_info = s3['bucket']
    bucket_name = bucket_info['name']

    record_to_persist = {
        'device_day_id': device_id + '/' + day_date,
        'timestamp': timestamp_int,
        's3_uri': 's3://' + bucket_name + '/' + key,
    }
    persist_record(record_to_persist)

def persist_record(record):
    boto3.setup_default_session()
    table_name = os.environ['DYNAMO_TARGET_TABLE_NAME']
    dynamodb_client = boto3.client("dynamodb")
    item = {
        'DeviceDayId': { 'S': record['device_day_id']},
        'S3URI': { 'S': record['s3_uri']},
        'Timestamp': { 'N':  str(record['timestamp']) }
    }
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error persisting items")
