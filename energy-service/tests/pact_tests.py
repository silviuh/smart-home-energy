# energy-service/tests/pact_tests.py
import pytest
from pact import Consumer, Provider
import requests
import json

pact_device = Consumer('EnergyService').has_pact_with(Provider('DeviceService'))

@pytest.fixture(scope='module')
def device_pact(request):
    pact_device.start_service()
    yield pact_device
    pact_device.stop_service()

def test_get_device_for_energy_consumption(device_pact):
    expected = {
        'id': '12345',
        'name': 'Smart Thermostat',
        'type': 'thermostat'
    }

    (device_pact
     .given('a device with id 12345 exists')
     .upon_receiving('a request for device 12345')
     .with_request('GET', '/devices/12345')
     .will_respond_with(200, body=expected))

    with device_pact:
        response = requests.get(f"{device_pact.uri}/devices/12345")
    
    assert response.status_code == 200
    assert response.json() == expected

# Add more tests as needed