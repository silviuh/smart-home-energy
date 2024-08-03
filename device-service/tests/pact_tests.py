# energy-service/tests/pact_tests.py
import pytest
from pact import Consumer, Provider
import requests
import json

pact = Consumer('EnergyService').has_pact_with(Provider('DeviceService'))

@pytest.fixture(scope='module')
def pact_setup(request):
    pact.start_service()
    yield
    pact.stop_service()

def test_get_device(pact_setup):
    expected = {
        'id': '12345',
        'name': 'Smart Thermostat',
        'type': 'thermostat',
        'energy_consumption': 50
    }

    (pact
     .given('a device with id 12345 exists')
     .upon_receiving('a request for device 12345')
     .with_request('GET', '/devices/12345')
     .will_respond_with(200, body=expected))

    with pact:
        response = requests.get(f"{pact.uri}/devices/12345")
    
    assert response.status_code == 200
    assert response.json() == expected

def test_get_all_devices(pact_setup):
    expected = [
        {'id': '12345', 'name': 'Smart Thermostat', 'type': 'thermostat', 'energy_consumption': 50},
        {'id': '67890', 'name': 'Smart Light', 'type': 'light', 'energy_consumption': 10}
    ]

    (pact
     .given('devices exist')
     .upon_receiving('a request for all devices')
     .with_request('GET', '/devices')
     .will_respond_with(200, body=expected))

    with pact:
        response = requests.get(f"{pact.uri}/devices")
    
    assert response.status_code == 200
    assert response.json() == expected

# Run with: pytest pact_tests.py