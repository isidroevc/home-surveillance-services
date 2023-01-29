import boto3
import json
import os

async def send_message_to_queue(message):
    try:
        sqs = boto3.client('sqs')

        queue_url = os.environ['OUTPUT_SQS_QUEUE_URL']
        print(queue_url)
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )

        print("Message ID: " + response['MessageId'])
        return {
            'success': True,
            'response': response
        }
    except Exception as err:
        print(err)
        print("An error ocurred while sending message to queue")
        return {
            'success': False
        }

def delete_message_from_input_queue(receipt_handle):
    sqs = boto3.client('sqs')

    queue_url = os.environ['INPUT_SQS_QUEUE_URL']
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

