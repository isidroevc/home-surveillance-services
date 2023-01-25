import asyncio
async def handle_sqs_records(sqs_records):
    futures = []
    for sqs_record in sqs_records:
        futures.append(handle_sqs_record(sqs_record))
    await asyncio.gather(*futures)

async def handle_sqs_record(sqs_record):
    if not('body' in sqs_record):
        return
        
    parsed_body = json.loads(sqs_record['body'])
    if not('Records' in parsed_body):
        return
    handle_s3_records(parsed_body['Records'])