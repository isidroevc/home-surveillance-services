import boto3
import os
import json
from datetime import datetime

# Create an S3 access object
s3 = boto3.client("s3")
now  = datetime.utcnow()
device_id= '2aa71c6372d942808c36aa42047531c9'
day_date = now.strftime('%Y_%m_%d')
file_name = str(int(now.timestamp())) + '.jpg'
key  = device_id + '/' + day_date + '/' + file_name
print("Key: " + key)
with open("./test.jpg", "rb") as f:
    response = s3.upload_fileobj(
        f,
        os.environ['PHOTOMOVE_BUCKET'],
        key
    )
    print(json.dumps(response))