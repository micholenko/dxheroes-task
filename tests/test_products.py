import pytest
from uuid import uuid4
from offers_sdk.client import OffersClient, OffersAPIError
from offers_sdk.models import Offer

@pytest.mark.asyncio
async def test_get_offers_success(mocker):
    mocker.patch("offers_sdk.client.AuthClient.refresh_access_token", return_value="token")

    mock_get = mocker.patch("httpx.AsyncClient.request")
    mock_get.return_value.status_code = 200
    mock_offer_id1 = str(uuid4())
    mock_offer_id2 = str(uuid4())
    mock_get.return_value.json = mocker.Mock(return_value=[
        {"id": mock_offer_id1, "price": 100, "items_in_stock": 10},
        {"id": mock_offer_id2, "price": 200, "items_in_stock": 5}
    ])

    client = OffersClient(refresh_token="token")
    offers = await client.get_offers("product-id")

    assert isinstance(offers, list)
    assert isinstance(offers[0], Offer)
    assert str(offers[0].id) == mock_offer_id1

@pytest.mark.asyncio
async def test_get_offers_error(mocker):
    mocker.patch("offers_sdk.client.AuthClient.refresh_access_token", return_value="token")

    mock_get = mocker.patch("httpx.AsyncClient.request")
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = "Not Found"

    client = OffersClient(refresh_token="token")

    with pytest.raises(OffersAPIError):
        await client.get_offers("nonexistent-id")
