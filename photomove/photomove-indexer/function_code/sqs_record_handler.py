import asyncio
import boto3
import json
import os
def extract_photo_information(body):
    s3 = body['s3']
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

    return {
        'device_day_id': device_id + '/' + day_date,
        'timestamp': timestamp_int,
        's3_uri': 's3://' + bucket_name + '/' + key,
    }

def persist_photo_information(photo_information):
    boto3.setup_default_session()
    table_name = os.environ['DYNAMO_TARGET_TABLE_NAME']
    dynamodb_client = boto3.client("dynamodb")
    item = {
        'DeviceDayId': { 'S': photo_information['device_day_id']},
        'S3URI': { 'S': photo_information['s3_uri']},
        'Timestamp': { 'N':  str(photo_information['timestamp']) }
    }
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error persisting items")

def delete_message_from_input_queue(receipt_handle):
    sqs = boto3.client('sqs')

    queue_url = os.environ['INPUT_SQS_QUEUE_URL']
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )



async def handle_incoming_queue_message(message):
    try:
        print("Message: " + json.dumps(message))
        receipt_handle = message['receiptHandle']
        body = json.loads(message['body'])
        photo_information = extract_photo_information(body)
        persist_photo_information(photo_information)

        delete_message_from_input_queue(receipt_handle)

        return True
    except Exception as err:
        print(err)
        return False


async def handle_incoming_queue_messages(messages):
    async_jobs = []
    for message in messages:
        async_jobs.append(handle_incoming_queue_message(message))
    
    results = await asyncio.gather(*async_jobs)
    print("Results: ", results)
    if False in results: return False

    return True