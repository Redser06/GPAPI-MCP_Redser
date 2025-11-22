"""Centralized authentication and token management for GlobalPayments API."""

import hashlib
import time
import os
import sys
from typing import Optional, Dict
import requests


class TokenManager:
    """Singleton token manager with caching and automatic refresh."""
    
    _instance = None
    _token_cache: Dict[str, str] = {}
    _token_expiry: Dict[str, float] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.app_id = os.getenv("GP_APP_ID")
        self.app_key = os.getenv("GP_APP_KEY")
        self.environment = os.getenv("GP_ENVIRONMENT", "sandbox")
        
        if not self.app_id or not self.app_key:
            print("WARNING: GP_APP_ID or GP_APP_KEY not set", file=sys.stderr)
    
    def _generate_token(self, scope: Optional[str] = None) -> str:
        """Generate a new access token from GlobalPayments."""
        if not self.app_id or not self.app_key:
            raise ValueError("GP_APP_ID or GP_APP_KEY not configured")
        
        nonce = str(int(time.time() * 1000))
        secret_raw = nonce + self.app_key
        secret = hashlib.sha512(secret_raw.encode()).hexdigest()
        
        base_url = (
            "https://apis.sandbox.globalpay.com" 
            if self.environment == "sandbox" 
            else "https://apis.globalpay.com"
        )
        url = f"{base_url}/ucp/accesstoken"
        
        headers = {
            "Content-Type": "application/json",
            "X-GP-Version": "2021-03-22"
        }
        
        payload = {
            "app_id": self.app_id,
            "nonce": nonce,
            "secret": secret,
            "grant_type": "client_credentials"
        }
        
        if scope:
            payload["scope"] = scope
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("token")
    
    def get_token(self, scope: Optional[str] = None, force_refresh: bool = False) -> str:
        """
        Get a valid access token, using cache when possible.
        
        Args:
            scope: Optional scope for the token
            force_refresh: Force generation of a new token
            
        Returns:
            Valid access token
        """
        cache_key = scope or "default"
        
        # Check cache unless force refresh
        if not force_refresh and cache_key in self._token_cache:
            # Check if token is still valid (tokens typically last 1 hour, we refresh at 55 min)
            if time.time() < self._token_expiry.get(cache_key, 0):
                return self._token_cache[cache_key]
        
        # Generate new token
        token = self._generate_token(scope)
        
        # Cache token (expire in 55 minutes)
        self._token_cache[cache_key] = token
        self._token_expiry[cache_key] = time.time() + (55 * 60)
        
        return token
    
    def invalidate_cache(self, scope: Optional[str] = None):
        """Invalidate cached token(s)."""
        if scope:
            self._token_cache.pop(scope, None)
            self._token_expiry.pop(scope, None)
        else:
            self._token_cache.clear()
            self._token_expiry.clear()
    
    @property
    def base_url(self) -> str:
        """Get the base URL for API requests."""
        return (
            "https://apis.sandbox.globalpay.com" 
            if self.environment == "sandbox" 
            else "https://apis.globalpay.com"
        )
