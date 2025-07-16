import pytest
from uuid import uuid4
from offers_sdk.client import OffersClient, OffersAPIError
from offers_sdk.models import Product

@pytest.mark.asyncio
async def test_register_product_success(mocker):
    mock_token = "access-token"
    mock_product_id = str(uuid4())

    # Patch AuthClient
    mocker.patch("offers_sdk.client.AuthClient.refresh_access_token", return_value=mock_token)

    # Patch POST request
    mock_post = mocker.patch("httpx.AsyncClient.request")
    mock_post.return_value.status_code = 201
    mock_post.return_value.json = mocker.Mock(return_value={
        "id": mock_product_id,
        "name": "Test Product",
        "description": "Test Desc"
    })

    client = OffersClient(refresh_token="token")
    product = await client.register_product("Test Product", "Test Desc")

    assert isinstance(product, Product)
    assert str(product.id) == mock_product_id
    assert product.name == "Test Product"

@pytest.mark.asyncio
async def test_register_product_error(mocker):
    mocker.patch("offers_sdk.client.AuthClient.refresh_access_token", return_value="token")

    mock_post = mocker.patch("httpx.AsyncClient.request")
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Bad Request"

    client = OffersClient(refresh_token="token")

    with pytest.raises(OffersAPIError):
        await client.register_product("Bad", "Fail case")
