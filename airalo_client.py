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

    def get_token(self) -> str | None:
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

    def submit_order(self, package_id: str, quantity: int, auth_token = None) -> dict:
        """Method to submit an order for eSIMs.

        Args:
            package_id (str): The ID of the package to order.
            quantity (int): Number of eSIMs to order.
            auth_token (str, optional): An existing access token. If not provided, a new token will be generated.
        
        Raises:
            ValueError: If the access token is not generated or if the HTTP response status is not 200.

        Returns:
            dict:
                {"submit_order_response": The JSON response from the API,
                "order_id": The ID of the submitted order}
        """
        if not 1 <= quantity <= 50:  # Based on the documentation.
            raise ValueError(f"Invalid quantity: {quantity}. It must be an integer between 1 and 50")
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
            submit_order_response = response.json()
            order_id = submit_order_response["data"]["id"]
            return {"submit_order_response": submit_order_response, "order_id": order_id}
        raise ValueError(f"HTTP response error: {response.status_code}")

    def get_esims(self, order_id, auth_token = None) -> list:
        """Method to retrieve a list of eSIMs previously ordered.

        Args:
            order_id: The ID of the order for which to retrieve eSIMs.
            auth_token (str, optional): An existing access token. If not provided, a new token will be generated.
        
        Raises:
            ValueError: If the access token is not generated or if the HTTP response status is not 200.

        Returns:
            list: The eSIMs from the order that corresponds to `order_id`.
        """
        if not auth_token:
            token = self.get_token()
            if not token:
                raise ValueError("Access token not generated.")
        else:
            token = auth_token

        esims_url = f"{self.base_url}/v2/sims?include=order&limit=100"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"}
        response = requests.get(esims_url, headers=headers)

        if response.status_code == 200:
            esims = response.json()["data"]
            esims_ordered = [esim for esim in esims if esim["simable"]["id"] == order_id]
            return esims_ordered
        raise ValueError(f"HTTP response error: {response.status_code}")
