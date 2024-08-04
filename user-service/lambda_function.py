# user-service/lambda_function.py
import json
import boto3
from boto3.dynamodb.conditions import Key
import requests

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('Users')
device_service_url = 'https://your-api-gateway-url.execute-api.region.amazonaws.com/stage'

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    
    if http_method == 'POST' and path == '/users':
        return create_user(json.loads(event['body']))
    elif http_method == 'GET' and path.startswith('/users/'):
        user_id = path.split('/')[-1]
        return get_user(user_id)
    elif http_method == 'POST' and path.startswith('/users/'):
        parts = path.split('/')
        user_id = parts[-2]
        if parts[-1] == 'devices':
            return add_device_to_user(user_id, json.loads(event['body']))
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request')
        }

def create_user(user_data):
    user_table.put_item(Item=user_data)
    return {
        'statusCode': 201,
        'body': json.dumps(user_data)
    }

def get_user(user_id):
    response = user_table.get_item(Key={'id': user_id})
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('User not found')
        }

def add_device_to_user(user_id, device_data):
    # Validate device exists
    device_response = requests.get(f"{device_service_url}/devices/{device_data['device_id']}")
    if device_response.status_code != 200:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid device')
        }
    
    user_table.update_item(
        Key={'id': user_id},
        UpdateExpression="SET devices = list_append(if_not_exists(devices, :empty_list), :device)",
        ExpressionAttributeValues={
            ':empty_list': [],
            ':device': [device_data['device_id']]
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Device added to user')
    }