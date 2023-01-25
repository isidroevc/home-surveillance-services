import json
from record_handler import handle_records
def lambda_handler(event, context):
    if not('Records' in event):
        return {
            'statusCode': 200,
            'body': json.dumps('Nothing to be done')
        }
    records = event['Records']
    for record in records:
        if not('body' in record):
            print("All gone")
            continue
        parsed_body = json.loads(record['body'])
        print(parsed_body)
        if not('Records' in parsed_body):
            continue
        print("Handled some records")
        handle_records(parsed_body['Records'])
    
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }

