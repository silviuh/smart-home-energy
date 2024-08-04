# device-service/lambda_function.py
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Devices')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    
    if http_method == 'GET' and path == '/devices':
        return get_devices()
    elif http_method == 'POST' and path == '/devices':
        return add_device(json.loads(event['body']))
    elif http_method == 'GET' and path.startswith('/devices/'):
        device_id = path.split('/')[-1]
        return get_device(device_id)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request')
        }

def get_devices():
    response = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }

def add_device(device_data):
    table.put_item(Item=device_data)
    return {
        'statusCode': 201,
        'body': json.dumps(device_data)
    }

def get_device(device_id):
    response = table.query(
        KeyConditionExpression=Key('id').eq(device_id)
    )
    if response['Items']:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'][0])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Device not found')
        }
    
# device-service/lambda_function.py
# Add this to the existing lambda_function.py

def handle_provider_state(state):
    if state == 'a device with id 12345 exists':
        table.put_item(Item={
            'id': '12345',
            'name': 'Smart Thermostat',
            'type': 'thermostat'
        })
    elif state == 'a device with id 67890 exists':
        table.put_item(Item={
            'id': '67890',
            'name': 'Smart Light',
            'type': 'light'
        })

def lambda_handler(event, context):
    # ... existing code ...

    if http_method == 'POST' and path == '/_pact/provider_states':
        body = json.loads(event['body'])
        handle_provider_state(body['state'])
        return {
            'statusCode': 200,
            'body': json.dumps({'setup': True})
        }

    # ... rest of existing code ...