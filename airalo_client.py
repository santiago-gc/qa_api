import requests

class AiraloApiClient:
    """Client for interacting with the Airalo Partner API."""

    def __init__(self, client_id, client_secret, base_url="https://sandbox-partners-api.airalo.com"):
        """Initializes the AiraloApiClient.

        Args:
            client_id: The client ID for OAuth2 authentication.
            client_secret: The client secret for OAuth2 authentication.
            base_url: The base URL of the Airalo Partner API.
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def get_token(self):
        """Method to obtain an OAuth2 token from the Airalo API.

        Returns:
            The access token as a string, or `None` if the request fails.
        """
        token_url = f"{self.base_url}/v2/token"
        headers = {"Content-Type": "application/json"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(token_url, headers=headers, json=payload)

        if response.status_code == 200:
            self.token = response.json()["data"]["access_token"]
            return self.token
        return None

    def submit_order(self, package_id: str, quantity: int, auth_token = None):
        """Method to submit an order for eSIMs.

        Args:
            package_id (str): The ID of the package to order.
            quantity (int): Number of eSIMs to order.
            auth_token (str, optional): An existing access token. If not provided, a new token will be generated.
        
        Raises:
            ValueError: If the access token is not generated or if the HTTP response status is not 200.

        Returns:
            The JSON response from the API.
        """
        if not auth_token:
            token = self.get_token()
            if not token:
                raise ValueError("Access token not generated.")
        else:
            token = auth_token

        order_url = f"{self.base_url}/v2/orders"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",            
        }
        payload = {
            "package_id": package_id,
            "quantity": quantity,
        }
        response = requests.post(order_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        raise ValueError(f"HTTP response error: {response.status_code}")

    def get_esims(self, auth_token = None):
        """Method to retrieve a list of available eSIMs.

        Args:
            auth_token (str, optional): An existing access token. If not provided, a new token will be generated.
        
        Raises:
            ValueError: If the access token is not generated or if the HTTP response status is not 200.

        Returns:
            The JSON response from the API.
        """
        if not auth_token:
            token = self.get_token()
            if not token:
                raise ValueError("Access token not generated.")
        else:
            token = auth_token

        esims_url = f"{self.base_url}/v2/sims"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"}
        response = requests.get(esims_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        raise ValueError(f"HTTP response error: {response.status_code}")
