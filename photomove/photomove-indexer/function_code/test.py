import json
from lambda_function import lambda_handler

with open('../example-events/new_photo.example.json', 'r') as fcc_file:
    event = json.load(fcc_file)
    print(lambda_handler(event, 'context'))
