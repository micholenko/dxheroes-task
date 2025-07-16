import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
import httpx
from .config import AUTH_URL

TOKEN_FILE = Path(".offers_token_cache.json")

class AuthenticationError(Exception):
    """Custom exception raised when authentication fails."""
    pass

class AuthClient:
    """
    Handles authentication using a refresh token and caches the access token.
    """

    def __init__(self, refresh_token: str):
        """
        Initialize the AuthClient.

        Parameters:
            refresh_token (str): The refresh token for obtaining access tokens.
        """
        self.refresh_token = refresh_token
        self.access_token: Optional[str] = None
        self.expires_at: Optional[datetime] = None
        self._load_token_from_file()

    def _load_token_from_file(self):
        """
        Load access token and expiration time from a cache file, if available.
        """
        if TOKEN_FILE.exists():
            try:
                data = json.loads(TOKEN_FILE.read_text())
                self.access_token = data["access_token"]
                expires_at = datetime.fromisoformat(data["expires_at"])
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                self.expires_at = expires_at
            except Exception:
                pass

    def _save_token_to_file(self):
        """
        Save the current access token and expiration time to a cache file.
        """
        if self.access_token and self.expires_at:
            data = {
                "access_token": self.access_token,
                "expires_at": self.expires_at.isoformat()
            }
            TOKEN_FILE.write_text(json.dumps(data))

    async def refresh_access_token(self, using_cache: bool = True) -> str:
        """
        Refresh and return a valid access token.

        If a valid cached token exists and using_cache is True, it is returned.
        Otherwise, a new token is requested from the API.

        Parameters:
            using_cache (bool): Whether to use a cached token if available.

        Returns:
            str: The access token.

        Raises:
            AuthenticationError: If the token refresh request fails.
        """
        now = datetime.now(timezone.utc)
        if using_cache and self.access_token and self.expires_at and now < self.expires_at:
            return self.access_token

        async with httpx.AsyncClient() as client:
            response = await client.post(AUTH_URL, headers={"Bearer": self.refresh_token})
            
            if response.status_code != 201:
                raise AuthenticationError("Failed to refresh access token")

            data = response.json()
            self.access_token = data["access_token"]
            self.expires_at = now + timedelta(minutes=4.9)  # Slight buffer
            self._save_token_to_file()
            return self.access_token
