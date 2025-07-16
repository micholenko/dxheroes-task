import pytest
from offers_sdk.auth import AuthClient, AuthenticationError
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_auth_token_refresh_success(mocker):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value.status_code = 201
    mock_post.return_value.json = mocker.Mock(return_value={"access_token": "new-token"})

    auth = AuthClient(refresh_token="valid-refresh")
    token = await auth.refresh_access_token(using_cache=False)

    assert token == "new-token"
    assert auth.access_token == "new-token"
    assert auth.expires_at is not None

@pytest.mark.asyncio
async def test_auth_invalid_refresh_token_raises_error(mocker):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Invalid refresh token"

    auth = AuthClient(refresh_token="invalid-refresh")

    with pytest.raises(AuthenticationError):
        await auth.refresh_access_token(using_cache=False)