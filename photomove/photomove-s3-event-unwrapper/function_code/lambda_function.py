import json
import asyncio
from handle_queue_messages import handle_incoming_queue_messages
def lambda_handler(event, context):
    if not('Records' in event) or len(event['Records']) == 0:
        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
    result = asyncio.run(handle_incoming_queue_messages(event['Records']))
    print(result)
    if not(result):
        raise Exception("Failed to process some items")
    
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }

