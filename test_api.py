import os
import pytest
from dotenv import load_dotenv
from airalo_client import AiraloApiClient

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
PACKAGE_ID = "merhaba-7days-1gb"
QUANTITY = 6

@pytest.fixture(scope="module")
def api_client():
    """Fixture to create an instance of the AiraloApiClient."""
    return AiraloApiClient(CLIENT_ID, CLIENT_SECRET)

def test_get_token(api_client):
    """Test to get an OAuth2 token from the Airalo API."""
    token = api_client.get_token()
    assert token

def test_submit_order(api_client):
    """Test to verify an eSIM order submision based on quantity and package_id."""
    order_response = api_client.submit_order(PACKAGE_ID, QUANTITY)
    response_package_id = order_response["data"]["package_id"]
    response_quantity = order_response["data"]["quantity"]
    assert response_package_id == PACKAGE_ID
    assert len(order_response["data"]["sims"]) == QUANTITY
    assert response_quantity == QUANTITY

def test_get_esims(api_client):
    """Test to retrieve a list of eSIMs and validate them."""
    token = api_client.get_token()    
    order = api_client.submit_order(PACKAGE_ID, QUANTITY, token)
    order_id = order["data"]["id"]
    get_esims = api_client.get_esims(token)
    
    esims_ordered = order["data"]["sims"]
    get_esims_data = get_esims["data"]    
    
    get_esims_ids = []
    for esim in get_esims_data:
        get_esims_ids.append(esim["id"])
    get_esims_ids.sort()

    for esim_ordered in esims_ordered:
        assert esim_ordered["id"] in get_esims_ids
