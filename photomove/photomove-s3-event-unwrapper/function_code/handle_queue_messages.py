import json
import asyncio
from send_message import send_message_to_queue, delete_message_from_input_queue

async def handle_incoming_queue_message(queue_message):
    if not('body' in queue_message):
        print("Queue message has not body")
        return False
    
    if not('receiptHandle' in queue_message):
        print("Queue message has not receiptHandle")
        return False

    body = json.loads(queue_message['body'])
    if not('Records' in body):
        print("Queue message body has not Records")
        return False

    records = body['Records']
    async_jobs = []
    for message in records:
        print(message)
        async_jobs.append(send_message_to_queue(message)) 
    
    results = await asyncio.gather(*async_jobs)
    for result in results:
        if not(result['success']):
            return False
    delete_message_from_input_queue(queue_message['receiptHandle'])
    return True

async def handle_incoming_queue_messages(queue_messages):
    async_jobs = []
    for message in queue_messages:
        async_jobs.append(handle_incoming_queue_message(message)) 
    
    results = await asyncio.gather(*async_jobs)
    for result in results:
        if not(result):
            return False
        
    return True 


