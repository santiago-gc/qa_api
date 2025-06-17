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
    """Fixture to create an instance of AiraloApiClient"""
    return AiraloApiClient(CLIENT_ID, CLIENT_SECRET)

def test_get_token(api_client):
    """Test to get an OAuth2 token from the Airalo API"""
    token = api_client.get_token()
    assert token

def submit_order(api_client, quantity):
    """Function to verify an eSIM order submision based on quantity and package_id"""
    order_response = api_client.submit_order(PACKAGE_ID, quantity)["submit_order_response"]
    response_package_id = order_response["data"]["package_id"]
    response_quantity = order_response["data"]["quantity"]
    assert response_package_id == PACKAGE_ID
    assert len(order_response["data"]["sims"]) == quantity
    assert response_quantity == quantity

def test_submit_order_1eSIM(api_client):
    """Test to verify 1 eSIM order submision."""
    submit_order(api_client, 1)

def test_submit_order_6eSIM(api_client):
    """Test to verify 6 eSIMs order submision."""
    submit_order(api_client, QUANTITY)

def test_submit_order_50eSIM(api_client):
    """Test to verify 50 eSIMs order submision."""
    submit_order(api_client, 50)

def test_get_esims(api_client):
    """Test to retrieve a list of eSIMs and validate that they correspond to a previously submitted order"""
    token = api_client.get_token()    
    order = api_client.submit_order(PACKAGE_ID, QUANTITY, token)
    order_response = order["submit_order_response"]
    order_id = order["order_id"]
    get_esims = api_client.get_esims(order_id, token)
    esims_ordered = order_response["data"]["sims"]
    esims_ordered_ids = [esim["id"] for esim in esims_ordered]
    assert len(esims_ordered) == QUANTITY
    assert len(get_esims) == QUANTITY
    for esim_in_list in get_esims:
        assert esim_in_list["id"] in esims_ordered_ids
        assert esim_in_list["simable"]["package_id"] == PACKAGE_ID

@pytest.mark.xfail(reason="The quantity value must be an ineger between 1 and 50")
def test_fail_submit_order_0eSIM(api_client):
    """Test to verify 0 eSIMs order submision."""
    submit_order(api_client, 0)

@pytest.mark.xfail(reason="The quantity value must be an ineger between 1 and 50")
def test_fail_submit_order_51eSIM(api_client):
    """Test to verify 51 eSIMs order submision."""
    submit_order(api_client, 51)
