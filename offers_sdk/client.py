import httpx
import uuid
from .auth import AuthClient
from .models import Product, Offer
from .config import BASE_URL
from typing import List

class OffersAPIError(Exception):
    """Custom exception for Offers API errors."""
    pass

class OffersClient:
    """Client for interacting with the Offers API."""

    def __init__(self, refresh_token: str):
        """
        Initialize OffersClient with a refresh token.

        Parameters:
            refresh_token (str): The refresh token for authentication.
        """
        self.auth_client = AuthClient(refresh_token)
        self.client = httpx.AsyncClient()

    async def _get_headers(self):
        """
        Get authorization headers with a fresh access token.

        Returns:
            dict: Headers containing the Bearer token.
        """
        token = await self.auth_client.refresh_access_token()
        return {"Bearer": token}

    async def _request_with_auth(self, method: str, url: str, **kwargs):
        """
        Make an authenticated HTTP request, retrying once on 401.

        Parameters:
            method (str): HTTP method (e.g., 'GET', 'POST').
            url (str): The request URL.
            **kwargs: Additional arguments for the request.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            OffersAPIError: If the request fails with status >= 400.
        """
        headers = await self._get_headers()
        response = await self.client.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:
            # Force refresh and retry once
            await self.auth_client.refresh_access_token()
            headers = await self._get_headers()
            response = await self.client.request(method, url, headers=headers, **kwargs)

        if response.status_code >= 400:
            raise OffersAPIError(f"{method} {url} failed: {response.status_code} - {response.text}")

        return response

    async def register_product(self, name: str, description: str) -> Product:
        """
        Register a new product and return the Product object.

        Parameters:
            name (str): The name of the product.
            description (str): The description of the product.

        Returns:
            Product: The registered product object.
        """
        url = f"{BASE_URL}/products/register"
        product_id = str(uuid.uuid4())
        response = await self._request_with_auth("POST", url, json={"id": product_id, "name": name, "description": description})
        data = response.json()
        return Product(
            id=data['id'],
            name=name,
            description=description
        )

    async def get_offers(self, product_id: str) -> List[Offer]:
        """
        Get a list of offers for a given product.

        Parameters:
            product_id (str): The ID of the product.

        Returns:
            List[Offer]: A list of offers for the product.
        """
        url = f"{BASE_URL}/products/{product_id}/offers"
        response = await self._request_with_auth("GET", url)
        data = response.json()
        return [Offer(**offer) for offer in data]