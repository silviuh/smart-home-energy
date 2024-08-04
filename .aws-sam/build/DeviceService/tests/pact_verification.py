# device-service/tests/pact_verification.py

import pytest
from pact import Verifier
import os
import boto3
from moto import mock_dynamodb
import json
import tempfile

# Import your lambda function
from lambda_function import lambda_handler

# These would typically be set as environment variables in your CI/CD pipeline
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
PACT_BUCKET_NAME = os.environ.get('PACT_BUCKET_NAME', 'your-pact-bucket-name')
DEVICES_TABLE_NAME = os.environ.get('DEVICES_TABLE_NAME', 'Devices')

@pytest.fixture(scope='session')
def mock_dynamodb_table():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.create_table(
            TableName=DEVICES_TABLE_NAME,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        yield table

@pytest.fixture(scope='session')
def pact_verifier(mock_dynamodb_table):
    return Verifier(
        provider="DeviceService",
        provider_base_url="http://localhost:3000"  # This URL is not used but required
    )

def download_pact_files():
    s3 = boto3.client('s3', region_name=AWS_REGION)
    pact_files = []

    # Create a temporary directory to store downloaded pact files
    with tempfile.TemporaryDirectory() as tmpdirname:
        # List objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=PACT_BUCKET_NAME, Prefix='pacts/')
        
        for obj in response.get('Contents', []):
            if obj['Key'].endswith('.json'):
                local_file_path = os.path.join(tmpdirname, os.path.basename(obj['Key']))
                s3.download_file(PACT_BUCKET_NAME, obj['Key'], local_file_path)
                pact_files.append(local_file_path)

    return pact_files

def test_device_service_provider(pact_verifier, mock_dynamodb_table):
    def lambda_handler_wrapper(event, context):
        # Convert API Gateway format to Lambda format
        if 'requestContext' in event and 'http' in event['requestContext']:
            path_parameters = {}
            resource_path = event['requestContext']['http']['path']
            path_parts = resource_path.split('/')
            if len(path_parts) > 2 and path_parts[1] == 'devices':
                path_parameters['device_id'] = path_parts[2]
            
            lambda_event = {
                'httpMethod': event['requestContext']['http']['method'],
                'path': event['requestContext']['http']['path'],
                'pathParameters': path_parameters,
                'body': event.get('body', '{}')
            }
        else:
            lambda_event = event

        # Call the actual lambda handler
        response = lambda_handler(lambda_event, context)
        
        # Convert Lambda response format to API Gateway format
        return {
            'statusCode': response['statusCode'],
            'body': response['body']
        }

    def setup_states(provider_state):
        if provider_state == 'a device with id 12345 exists':
            mock_dynamodb_table.put_item(Item={
                'id': '12345',
                'name': 'Smart Thermostat',
                'type': 'thermostat'
            })
        elif provider_state == 'a device with id 67890 exists':
            mock_dynamodb_table.put_item(Item={
                'id': '67890',
                'name': 'Smart Light',
                'type': 'light'
            })

    # Download pact files from S3
    pact_files = download_pact_files()

    # Verify the pacts
    result = pact_verifier.verify_pacts(
        pact_files,
        provider_state_setup_callable=setup_states,
        provider_app_callable=lambda_handler_wrapper
    )

    assert result == 0, "Pact verification failed"

if __name__ == '__main__':
    pytest.main()